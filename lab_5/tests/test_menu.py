from lab_5 import main as app


def test_main_menu_runs_variant_16_and_saves_results(monkeypatch, capsys, tmp_path):
    answers = iter(["1", "16", "4"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))
    monkeypatch.setattr(app, "OUTPUT_DIR", tmp_path)

    app.main()

    output = capsys.readouterr().out
    assert "4. Выход" in output
    assert "Вариант: 16" in output
    assert "Факторизация n: p=193, q=293" in output
    assert "Открытый текст: M=2316" in output
    assert "Работа завершена." in output
    saved = (tmp_path / "variant_16_solution.txt").read_text(encoding="utf-8")
    assert "Закрытый показатель: d=38195" in saved


def test_custom_rsa_inputs_are_factored_and_decrypted(monkeypatch, capsys, tmp_path):
    answers = iter(["2", "3", "55", "23", "4"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))
    monkeypatch.setattr(app, "OUTPUT_DIR", tmp_path)

    app.main()

    output = capsys.readouterr().out
    assert "Факторизация n: p=5, q=11" in output
    assert "Закрытый показатель: d=27" in output
    assert "Открытый текст: M=12" in output
    saved = (tmp_path / "variant_custom_solution.txt").read_text(encoding="utf-8")
    assert "Шифротекст: C=23" in saved


def test_math_check_menu_displays_bezout_identity(monkeypatch, capsys):
    answers = iter(["3", "1", "240", "46", "0", "4"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

    app.main()

    output = capsys.readouterr().out
    assert "НОД(240, 46) = 2" in output
    assert "Проверка: 240·-9 + 46·47 = 2." in output


def test_math_check_menu_runs_pollard_rho_factorization(monkeypatch, capsys):
    answers = iter(["3", "4", "56549", "0", "4"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

    app.main()

    output = capsys.readouterr().out
    assert "4. Факторизация n методом Полларда rho" in output
    assert "Факторизация: n = p·q = 193·293 = 56549." in output
    assert "Итераций алгоритма Полларда rho:" in output
