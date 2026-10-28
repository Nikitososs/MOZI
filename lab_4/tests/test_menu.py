from lab_4 import main as app


def test_variant_16_is_a_separate_main_menu_action(monkeypatch, capsys, tmp_path):
    answers = iter(["3", "ВАСЯ МОЛОДЕЦ", "", "4"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))
    monkeypatch.setattr(app, "OUTPUT_DIR", tmp_path)

    app.main()

    output = capsys.readouterr().out
    assert "3. Выполнение варианта 16" in output
    assert "4. Выход" in output
    assert "ВЫПОЛНЕНИЕ ВАРИАНТА 16" in output
    assert "p=167, q=311" in output
    assert "Проверка пройдена: открытый текст восстановлен без изменений." in output
    saved = (tmp_path / "rsa_result.txt").read_text(encoding="utf-8")
    assert "Результат расшифрования: ВАСЯ МОЛОДЕЦ" in saved
