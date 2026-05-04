from importlib import reload
import player
from game import (
    choose_rule,
    generate_numbers,
    direction,
    guess_rule,
    verify_player_guess,
)

import datetime

try:
    from tqdm import tqdm
except ImportError:
    print("Tqdm não foi instalado. Instale com: python -m pip install tqdm")
    raise SystemExit(1)


def play_one_game(max_attempts):
    rule, _, rule_info = choose_rule()
    rule_type_original = rule_info["type"]
    numbers = generate_numbers(rule)

    reload(player)
    number_guesses = []
    rule_guesses = []
    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        guess = verify_player_guess(player.player(number_guesses, rule_guesses))

        if guess[0] == "NUMBER":
            n = guess[1]
            d = direction(n, numbers)
            hit = n in numbers
            number_guesses.append([n, d, hit])
            continue

        rule_type, p1, p2 = guess[1]
        if rule_type == "mod":
            guessed_rule = {"type": "mod", "k": p1, "r": p2}
        elif rule_type == "pot":
            guessed_rule = {"type": "pot", "p": p1}
        else:
            guessed_rule = {"type": "int", "a": p1, "b": p2}

        rule_guesses.append([rule_type, p1, p2])
        if guess_rule(guessed_rule, rule_info):
            return {"win": True, "attempts": attempts, "type": rule_type_original}

    return {"win": False, "attempts": max_attempts, "type": rule_type_original}


def results_from_list(values):
    if not values:
        return 0, 0, 0, 0, 0
    ordered = sorted(values)
    n = len(ordered)
    mean = sum(ordered) / n
    median = (
        ordered[n // 2] if n % 2 == 1 else (ordered[n // 2 - 1] + ordered[n // 2]) / 2
    )
    std = (sum((x - mean) ** 2 for x in ordered) / n) ** 0.5
    return mean, median, std, ordered[0], ordered[-1]


def update_readme(stats_by_type, total_games):
    """Gera a tabela Markdown completa e sobrescreve o README.md."""

    # Coletar dados globais
    all_attempts = []
    total_wins = 0
    for data in stats_by_type.values():
        all_attempts.extend(data["attempts"])
        total_wins += data["wins"]

    lines = [
        "## mc102-p1\n",
        "### Resultado do Último Torneio\n",
        "| Regra | Partidas | Vitórias | Win % | Média | Mediana | Desvio P. | Min | Max |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    # Linhas por tipo
    for r_type in ["mod", "pot", "int"]:
        data = stats_by_type[r_type]
        if data["count"] > 0:
            mean, median, std, v_min, v_max = results_from_list(data["attempts"])
            win_p = (data["wins"] / data["count"]) * 100
            lines.append(
                f"| {r_type.upper()} | {data['count']} | {data['wins']} | {win_p:.1f}% | {mean:.2f} | {median} | {std:.2f} | {v_min} | {v_max} |"
            )

    # Linha Global
    g_mean, g_median, g_std, g_min, g_max = results_from_list(all_attempts)
    g_win_p = (total_wins / total_games) * 100
    lines.append(
        f"| **GLOBAL** | **{total_games}** | **{total_wins}** | **{g_win_p:.1f}%** | **{g_mean:.2f}** | **{g_median}** | **{g_std:.2f}** | **{g_min}** | **{g_max}** |"
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n[OK] README.md atualizado com estatísticas detalhadas!")


def update_changelog(stats_by_type, total_games):
    """Adiciona os resultados atuais ao final do CHANGELOG.md com data e hora."""

    # Coletar dados globais
    all_attempts = []
    total_wins = 0
    for data in stats_by_type.values():
        all_attempts.extend(data["attempts"])
        total_wins += data["wins"]

    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    lines = [
        f"\n## Relatório de Execução - {now}\n",
        "| Regra | Partidas | Vitórias | Win % | Média | Mediana | Desvio P. | Min | Max |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    for r_type in ["mod", "pot", "int"]:
        data = stats_by_type[r_type]
        if data["count"] > 0:
            mean, median, std, v_min, v_max = results_from_list(data["attempts"])
            win_p = (data["wins"] / data["count"]) * 100
            lines.append(
                f"| {r_type.upper()} | {data['count']} | {data['wins']} | {win_p:.1f}% | {mean:.2f} | {median} | {std:.2f} | {v_min} | {v_max} |"
            )

    g_mean, g_median, g_std, g_min, g_max = results_from_list(all_attempts)
    g_win_p = (total_wins / total_games) * 100
    lines.append(
        f"| **GLOBAL** | **{total_games}** | **{total_wins}** | **{g_win_p:.1f}%** | **{g_mean:.2f}** | **{g_median}** | **{g_std:.2f}** | **{g_min}** | **{g_max}** |\n"
    )
    lines.append("---\n")  # Linha horizontal para separar as entradas

    with open("CHANGELOG.md", "a", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("[OK] CHANGELOG.md atualizado (histórico preservado)!")


def main():
    max_games = 1000
    max_attempts = 1000

    stats_by_type = {
        "mod": {"attempts": [], "wins": 0, "count": 0},
        "pot": {"attempts": [], "wins": 0, "count": 0},
        "int": {"attempts": [], "wins": 0, "count": 0},
    }

    for _ in tqdm(range(max_games)):
        result = play_one_game(max_attempts=max_attempts)
        r_type = result["type"]
        stats_by_type[r_type]["count"] += 1
        stats_by_type[r_type]["attempts"].append(result["attempts"])
        if result["win"]:
            stats_by_type[r_type]["wins"] += 1

    update_readme(stats_by_type, max_games)

    update_readme(stats_by_type, max_games)

    # Atualiza o CHANGELOG (Histórico)
    update_changelog(stats_by_type, max_games)


if __name__ == "__main__":
    main()
