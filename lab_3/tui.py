"""Экранный интерфейс для запуска анализа и просмотра результата."""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.events import Resize
from textual.widgets import (
    Button,
    Collapsible,
    DataTable,
    Footer,
    Header,
    Input,
    Select,
    Static,
    TabPane,
    TabbedContent,
    TextArea,
)
from textual_plotext import PlotextPlot

from common.io_utils import read_text_file
from lab_3.entropy import GramStatistics, analyze, prepare_text
from lab_3.main import OUTPUT, VARIANT, run_analysis


class EntropyApp(App[None]):
    """Интерфейс ввода, анализа, графика и прокручиваемых частот."""

    TITLE = "ЛР3 · Модель открытого текста"
    SUB_TITLE = "Энтропия k-грамм"
    ENABLE_COMMAND_PALETTE = True
    CSS = """
    Screen { layout: vertical; background: $surface; }
    Header { background: $primary-darken-2; }
    #toolbar {
        height: 4; padding: 0 1; align: center middle; background: $panel;
        border-bottom: solid $primary-darken-2;
    }
    #language { width: 20; height: 3; margin: 0 1 0 0; }
    #run { width: 17; height: 3; padding: 0 1; margin: 0 1 0 0; }
    #example { width: 22; height: 3; padding: 0 1; margin: 0; }
    #main-views { height: 1fr; min-height: 8; margin: 0 1; }
    #main-views > ContentSwitcher { height: 1fr; }
    #main-views TabPane { height: 1fr; padding: 1; }
    #input-area { height: 1fr; min-height: 5; border: round $primary; }
    #file-row { height: 3; padding: 0; margin-top: 1; }
    #file-path { width: 1fr; }
    #load { width: 18; margin-left: 1; }
    #output-row { height: 3; margin-top: 0; }
    #output-path { width: 1fr; }
    #input-hint { height: 2; color: $text-muted; padding: 0 1; }
    #prepared-collapse { height: auto; margin: 0 0 1 0; }
    #prepared-area { height: 6; min-height: 3; border: round $primary-darken-2; }
    #summary { height: 2; padding: 0 1; color: $success; text-style: bold; }
    #result-views { height: 1fr; min-height: 7; }
    #result-views > ContentSwitcher { height: 1fr; }
    #result-views TabPane { height: 1fr; padding: 0 1; }
    #chart { width: 1fr; height: 1fr; min-height: 5; background: $panel; }
    #k-filter { height: 3; padding: 0 1; }
    #k-select { width: 20; margin-right: 1; }
    #gram-table { height: 1fr; border: round $primary-darken-2; }
    DataTable > .datatable--header { background: $primary-darken-2; color: $text; text-style: bold; }
    #status { height: 1; padding: 0 1; color: $text-muted; }
    Footer { background: $panel; }
    """

    BINDINGS = [
        ("ctrl+enter", "analyze", "Анализировать"),
        ("ctrl+o", "open_plot", "PNG-график"),
        ("ctrl+q", "quit", "Выход"),
    ]

    def __init__(
        self, initial_file: Path | None = None, output: Path = OUTPUT, language: str = "ru"
    ):
        super().__init__()
        self.theme = "nord"
        self.initial_file = initial_file
        self.output = output
        self.language = language
        self.results: list[GramStatistics] = []
        self.original_text = ""
        self.last_run_dir: Path | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="toolbar"):
            yield Select(
                [("Русский", "ru"), ("English", "en")], value="ru", allow_blank=False, id="language"
            )
            yield Button("Посчитать", variant="primary", id="run")
            yield Button("Открыть вариант 16", id="example")
        with TabbedContent(initial="input-tab", id="main-views"):
            with TabPane("Текст", id="input-tab"):
                yield Static("Вставьте текст ниже или загрузите его из файла.", id="input-hint")
                yield TextArea(
                    id="input-area",
                    soft_wrap=True,
                    show_line_numbers=False,
                    placeholder="Введите или вставьте текст…",
                )
                with Collapsible(
                    title="Обработанный текст", collapsed=True, id="prepared-collapse"
                ):
                    yield TextArea(
                        read_only=True, soft_wrap=True, show_line_numbers=False, id="prepared-area"
                    )
                with Horizontal(id="file-row"):
                    yield Input(placeholder="Путь к текстовому файлу", id="file-path")
                    yield Button("Загрузить файл", id="load")
                with Horizontal(id="output-row"):
                    yield Input(
                        value=str(self.output),
                        placeholder="Папка для отчёта и результатов",
                        id="output-path",
                    )
            with TabPane("Результаты", id="results-tab"):
                yield Static(
                    "Пока нет результатов. Нажмите «Посчитать» на вкладке «Текст».", id="summary"
                )
                with TabbedContent(initial="chart-tab", id="result-views"):
                    with TabPane("График Hₖ/k", id="chart-tab"):
                        yield PlotextPlot(id="chart")
                    with TabPane("Частоты k-грамм", id="frequency-tab"):
                        with Horizontal(id="k-filter"):
                            yield Select(
                                [(f"k = {k}", k) for k in range(1, 6)],
                                value=1,
                                allow_blank=False,
                                id="k-select",
                            )
                            yield Static("Отсортировано по частоте; список можно прокручивать.")
                        yield DataTable(id="gram-table", zebra_stripes=True, cursor_type="row")
        yield Static("", id="status")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#language", Select).value = self.language
        self.query_one("#output-path", Input).value = str(self.output)
        self.query_one("#input-area", TextArea).focus()
        self.update_prepared_text()
        table = self.query_one("#gram-table", DataTable)
        table.add_columns("k-грамма", "Количество", "Частота")
        if self.initial_file:
            self.query_one("#file-path", Input).value = str(self.initial_file)
            self.load_file(self.initial_file)

    def set_status(self, message: str) -> None:
        self.query_one("#status", Static).update(message)

    def load_file(self, path: Path) -> None:
        try:
            text = read_text_file(str(path))
        except (OSError, UnicodeError) as exc:
            self.set_status(f"Не удалось открыть файл: {exc}")
            return
        self.query_one("#input-area", TextArea).text = text
        self.set_status(f"Загружено: {path} · {len(text)} символов")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run":
            self.action_analyze()
        elif event.button.id == "load":
            raw_path = self.query_one("#file-path", Input).value.strip().strip('"')
            if not raw_path:
                self.set_status("Укажите путь к файлу.")
                return
            self.load_file(Path(raw_path))
        elif event.button.id == "example":
            self.query_one("#language", Select).value = "ru"
            self.query_one("#file-path", Input).value = str(VARIANT)
            self.load_file(VARIANT)
            self.query_one("#main-views", TabbedContent).active = "input-tab"

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "k-select" and self.results:
            self.update_frequency_table(int(event.value))
        elif event.select.id == "language":
            self.update_prepared_text()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area.id == "input-area":
            self.update_prepared_text()

    def update_prepared_text(self) -> None:
        """Обновить отдельное поле очищенной строкой выбранного алфавита."""
        raw = self.query_one("#input-area", TextArea).text
        language = str(self.query_one("#language", Select).value)
        cleaned = prepare_text(raw, language) if raw else ""
        self.query_one("#prepared-area", TextArea).text = cleaned

    def action_analyze(self) -> None:
        raw = self.query_one("#input-area", TextArea).text
        language = str(self.query_one("#language", Select).value)
        output_text = self.query_one("#output-path", Input).value.strip().strip('"')
        if not output_text:
            self.set_status("Укажите папку для отчёта и результатов.")
            return
        output_dir = Path(output_text).expanduser()
        try:
            cleaned = prepare_text(raw, language)
            results = analyze(cleaned)
            # Пакетный запуск сохраняет те же CSV и PNG, не загрязняя экран выводом.
            with redirect_stdout(StringIO()):
                run_dir = run_analysis(raw, language, output_dir)
        except (OSError, UnicodeError, ValueError) as exc:
            self.set_status(f"Ошибка: {exc}")
            return

        self.original_text = raw
        self.results = results
        self.last_run_dir = run_dir
        n = len(cleaned)
        values = [
            f"{r.k}={r.normalized:.2f}" if r.normalized is not None else f"{r.k}:—" for r in results
        ]
        self.query_one("#summary", Static).update(
            f"{language.upper()} · {n} букв · исключено: {len(raw) - n}  Hₖ/k: "
            + " · ".join(values)
        )
        self.update_frequency_table(int(self.query_one("#k-select", Select).value))
        self.query_one("#main-views", TabbedContent).active = "results-tab"
        self.query_one("#result-views", TabbedContent).active = "chart-tab"
        self.call_after_refresh(self.refresh_chart)
        self.set_status(f"Готово · Результаты и график: {run_dir.resolve()}")

    def on_resize(self, event: Resize) -> None:
        """Подгонять размер графика под доступную область окна."""
        if self.results and self.query_one("#main-views", TabbedContent).active == "results-tab":
            self.call_after_refresh(self.refresh_chart)

    def refresh_chart(self) -> None:
        """Построить более плавный график в терминале с braille-разрешением Plotext."""
        chart = self.query_one("#chart", PlotextPlot)
        plt = chart.plt
        plt.clear_figure()
        valid = [r for r in self.results if r.normalized is not None]
        if not valid:
            chart.refresh()
            return
        xs = [r.k for r in valid]
        ys = [r.normalized for r in valid]
        plt.plot(xs, ys, marker="braille", color="cyan+")
        plt.scatter(xs, ys, marker="hd", color="white+")
        plt.title("Нормированная энтропия Hₖ/k")
        plt.xlabel("k — длина k-граммы")
        plt.ylabel("Бит на символ")
        plt.xlim(0.8, 5.2)
        plt.xticks([1, 2, 3, 4, 5])
        plt.ylim(0, max(1.0, max(ys) * 1.15))
        plt.grid(True, False)
        chart.refresh()

    def action_open_plot(self) -> None:
        """Открыть сохранённый matplotlib-график в просмотрщике изображений."""
        if self.last_run_dir is None:
            self.set_status("Сначала выполните расчёт — PNG-график появится в папке результатов.")
            return
        path = self.last_run_dir / "entropy.png"
        try:
            import os

            os.startfile(str(path))
        except (AttributeError, OSError) as exc:
            self.set_status(f"Не удалось открыть PNG: {exc} · Файл: {path.resolve()}")
            return
        self.set_status(f"Открыт график matplotlib: {path.resolve()}")

    def update_frequency_table(self, k: int) -> None:
        table = self.query_one("#gram-table", DataTable)
        table.clear()
        result = next((r for r in self.results if r.k == k), None)
        if result is None or not result.total:
            self.set_status(f"Для k={k} нет полных k-грамм.")
            return
        for gram, count in sorted(result.counts.items(), key=lambda item: (-item[1], item[0])):
            table.add_row(gram, str(count), f"{count / result.total:.6f}")
        self.set_status(
            f"k={k} · окон: {result.total} · различных k-грамм: {len(result.counts)} · "
            "таблица прокручивается колесом мыши или клавишами ↑/↓"
        )


def main() -> None:
    """Запустить TUI с пустым полем или сразу загрузить заданный файл."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, help="Предзагрузить файл в TUI")
    parser.add_argument("--language", choices=("ru", "en"), default="ru")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    app = EntropyApp(args.file, args.output, args.language)
    app.run()


if __name__ == "__main__":
    main()
