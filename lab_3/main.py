"""TUI и пакетный запуск: python -m lab_3.main."""

import argparse
import csv
from datetime import datetime
from pathlib import Path
import shutil

from common.io_utils import read_text_file
from lab_3.entropy import analyze, prepare_text

OUTPUT = Path(__file__).resolve().parent / "outputs"
VARIANT = Path(__file__).resolve().parent / "texts" / "variant_16.txt"


def save_plot(results, path: Path) -> None:
    """Сохранить ломаную Hk/k в PNG без открытия графического окна."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot([r.k for r in results],
            [r.normalized if r.normalized is not None else float("nan")
             for r in results], "o-", color="#215a96")
    ax.set(xlabel="k", ylabel="Hₖ/k, бит/символ",
           title="Энтропия k-грамм открытого текста", xticks=range(1, 6))
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def run_analysis(text: str, language: str, output: Path = OUTPUT) -> Path:
    """Вывести анализ и сохранить отдельный архив вычисления с графиком."""
    cleaned = prepare_text(text, language)
    results = analyze(cleaned)
    output.mkdir(parents=True, exist_ok=True)
    run_dir = output / datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
    run_dir.mkdir()
    lines = [f"Язык: {language}; букв после обработки: {len(cleaned)}",
             f"Очищенный текст: {cleaned}",
             "Перекрывающиеся k-граммы, шаг 1."]
    with (run_dir / "frequencies.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["k", "gram", "count", "probability"])
        for r in results:
            lines.append(f"\nk={r.k}; окон: {r.total}; различных: {len(r.counts)}")
            for gram, n in sorted(r.counts.items(), key=lambda x: (-x[1], x[0])):
                p = n / r.total
                lines.append(f"{gram}: {n}; p={p:.8f}")
                writer.writerow([r.k, gram, n, p])
    lines.append("\nk    Hk, бит    Hk/k, бит/символ")
    with (run_dir / "entropy.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["k", "windows", "unique", "Hk", "Hk/k"])
        for r in results:
            writer.writerow([r.k, r.total, len(r.counts), r.entropy, r.normalized])
            lines.append(f"{r.k}    {r.entropy:.8f}    {r.normalized:.8f}"
                         if r.entropy is not None else f"{r.k}    нет данных")
    lines.append(f"Hk: {[r.entropy for r in results]}")
    lines.append(f"Hk/k: {[r.normalized for r in results]}")
    content = "\n".join(lines)
    (run_dir / "analysis.txt").write_text(content, encoding="utf-8")
    (run_dir / "prepared.txt").write_text(cleaned, encoding="utf-8")
    save_plot(results, run_dir / "entropy.png")
    (run_dir / "input.txt").write_text(text, encoding="utf-8")
    # Обновить удобные ссылки на последний расчёт и совместимость отчёта.
    for name in ("analysis.txt", "prepared.txt", "frequencies.csv", "entropy.csv", "entropy.png", "input.txt"):
        shutil.copy2(run_dir / name, output / name)
    print(content)
    print(f"\nРезультаты этого расчёта сохранены: {run_dir.resolve()}")
    return run_dir


def main() -> None:
    """Выбрать интерактивный или воспроизводимый файловый режим."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path)
    parser.add_argument("--language", choices=("ru", "en"), default="ru")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        if args.file:
            run_analysis(read_text_file(str(args.file)), args.language, args.output)
        else:
            from lab_3.tui import EntropyApp
            EntropyApp(output=args.output, language=args.language).run()
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(1, f"Ошибка: {exc}\n")
    except (EOFError, KeyboardInterrupt):
        print("\nВвод завершён.")


if __name__ == "__main__":
    main()
