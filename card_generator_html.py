"""
card_generator_html.py
HTML + Playwright рендер карточек — точь в точь как дизайн.

УСТАНОВКА НА СЕРВЕРЕ:
  pip install playwright pillow
  playwright install --with-deps chromium

ИСПОЛЬЗОВАНИЕ:
  from card_generator_html import (
      generate_profile_card,
      generate_leaderboard_card,
      generate_duo_leaderboard_card,
      generate_match_result_card,
  )
  buf = generate_profile_card(username="Nelents", ...)
  # buf — io.BytesIO с PNG, отправь в telegram как photo

Если playwright не установлен — падает с понятной ошибкой.
"""
from __future__ import annotations
import io, os, tempfile
from typing import Optional

from card_templates import (
    profile_html, leaderboard_html, match_result_html,
    faceit_level, LEVEL_COLORS,
)

# ─── Playwright singleton ──────────────────────────────────────────────────────
_playwright = None
_browser    = None

def _get_browser():
    global _playwright, _browser
    try:
        if _browser is not None and _browser.is_connected():
            return _browser
    except Exception:
        pass
    # Recreate browser (first launch or after crash/disconnect)
    try:
        if _browser is not None:
            _browser.close()
    except Exception:
        pass
    try:
        if _playwright is not None:
            _playwright.stop()
    except Exception:
        pass
    _browser    = None
    _playwright = None
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError(
            "playwright не установлен. Запусти:\n"
            "  pip install playwright\n"
            "  playwright install --with-deps chromium"
        )
    _playwright = sync_playwright().start()
    _browser    = _playwright.chromium.launch(
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    return _browser


def _html_to_png(html: str, width: int = 1080, extra_height: int = 0) -> io.BytesIO:
    """Рендерит HTML через Playwright и возвращает PNG байты."""
    browser = _get_browser()
    page    = browser.new_page(viewport={"width": width + 40, "height": 800})
    page.set_content(html, wait_until="networkidle")

    # подождём загрузку Google Fonts если есть интернет
    try:
        page.wait_for_load_state("networkidle", timeout=3000)
    except Exception:
        pass

    # screenshot всего контента
    body = page.query_selector("body")
    png_bytes = body.screenshot()
    page.close()

    return io.BytesIO(png_bytes)


def close():
    """Закрыть браузер (вызвать при завершении бота)."""
    global _playwright, _browser
    if _browser:
        _browser.close()
        _browser = None
    if _playwright:
        _playwright.stop()
        _playwright = None


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC API — те же сигнатуры что и в card_generator.py
# ══════════════════════════════════════════════════════════════════════════════

def generate_profile_card(
    username: str = "Unknown",
    game_id: str = "",
    user_id: int = 0,
    elo: int = 1000,
    wins: int = 0,
    losses: int = 0,
    kills: int = 0,
    deaths: int = 0,
    assists: int = 0,
    is_premium: bool = False,
    is_admin: bool = False,
    global_rank: int = 0,
    league: str = "default",
    map_stats: list = None,
    recent: list = None,
    leaderboard: list = None,
    quals_stats=None,
    mvp_count: int = 0,
    is_verified: bool = False,
    duo_stats=None,
    avatar_bytes: bytes = None,
    active_frame=None,
    active_banner=None,
    active_background=None,
) -> io.BytesIO:
    html = profile_html(
        username=username, game_id=game_id, user_id=user_id,
        elo=elo, wins=wins, losses=losses, kills=kills,
        deaths=deaths, assists=assists, is_premium=is_premium,
        is_admin=is_admin, global_rank=global_rank, league=league,
        map_stats=map_stats, recent=recent, leaderboard=leaderboard,
        mvp_count=mvp_count, is_verified=is_verified,
        avatar_bytes=avatar_bytes,
        active_frame=active_frame,
        active_banner=active_banner,
        active_background=active_background,
    )
    return _html_to_png(html, width=1060)


def generate_leaderboard_card(
    players: list,
    title: str = "ЛУЧШИЕ ИГРОКИ",
    avatars: dict = None,
) -> io.BytesIO:
    html = leaderboard_html(players=players, title=title, avatars=avatars)
    return _html_to_png(html, width=1080)


def generate_duo_leaderboard_card(
    players: list,
    title: str = "2v2 ТОП",
    avatars: dict = None,
) -> io.BytesIO:
    return generate_leaderboard_card(players, title=title, avatars=avatars)


def generate_match_result_card(
    match_code: str = "",
    map_name: str = "",
    winner: str = "ct",
    score_w: int = 0,
    score_l: int = 0,
    players_ct: list = None,
    players_t: list = None,
    league: str = "Default",
    avatars: dict = None,
) -> io.BytesIO:
    html = match_result_html(
        match_code=match_code, map_name=map_name, winner=winner,
        score_w=score_w, score_l=score_l,
        players_ct=players_ct, players_t=players_t,
        league=league, avatars=avatars,
    )
    return _html_to_png(html, width=1060)


# ══════════════════════════════════════════════════════════════════════════════
# ТЕСТ — генерирует HTML файлы для просмотра в браузере
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    from card_templates import faceit_level

    # Profile — без калибровки
    html1 = profile_html(
        username="Nelents", game_id="13259288", elo=1000,
        wins=0, losses=0, kills=0, deaths=0, assists=0,
        mvp_count=0, global_rank=0, league="Default",
    )
    with open("preview_profile.html","w",encoding="utf-8") as f: f.write(html1)
    print("✅ preview_profile.html")

    # Profile — с данными
    html1b = profile_html(
        username="StichDarling", game_id="5781932544", elo=1180,
        wins=45, losses=20, kills=312, deaths=198, assists=87,
        is_premium=True, global_rank=2, mvp_count=7, league="Default",
        recent=[{"won":True},{"won":False},{"won":True},{"won":True},
                {"won":False},{"won":True},{"won":True},{"won":False}],
        map_stats=[
            {"map":"Sandstone","wins":12,"losses":4},
            {"map":"Zone 9",   "wins":8, "losses":6},
            {"map":"Rust",     "wins":15,"losses":5},
        ],
        leaderboard=[{"name":"StichDarling","elo":1180}],
    )
    with open("preview_profile_full.html","w",encoding="utf-8") as f: f.write(html1b)
    print("✅ preview_profile_full.html")

    # Leaderboard
    names = ["sosvart","Jambo","44Fauswq","asdsaddsd","qwensi","хайсу","low cortisol","папа веня","alice patrol","eraseme"]
    elos  = [2527,2449,2329,2102,2002,1934,1444,1434,1419,1331]
    ws    = [129,121,119,73,76,100,41,49,62,41]
    ls    = [17,22,21,17,8,48,13,43,36,17]
    kds   = [1.93,2.31,1.89,1.63,1.69,1.56,2.07,1.16,1.83,1.44]
    pls=[]
    for i in range(10):
        pls.append({
            "rank":i+1,"name":names[i],"elo":elos[i],"wins":ws[i],"losses":ls[i],
            "kd":kds[i],"kills":int(kds[i]*(ws[i]+ls[i])),
            "deaths":(ws[i]+ls[i]),
            "level":faceit_level(elos[i]),"uid":i,
            "is_premium":i<2,"is_admin":i==0,"is_verified":i%3==0,
        })
    html2 = leaderboard_html(pls,"ЛУЧШИЕ ИГРОКИ — Default")
    with open("preview_leaderboard.html","w",encoding="utf-8") as f: f.write(html2)
    print("✅ preview_leaderboard.html")

    # Match
    html3 = match_result_html(
        match_code="JODLPRU",map_name="Sandstone",winner="ct",
        score_w=16,score_l=9,league="Default",
        players_ct=[
            {"name":"дмитрий на киев","kills":22,"deaths":14,"assists":3,"elo":1065},
            {"name":"coldzero","kills":18,"deaths":11,"assists":5,"elo":1089},
            {"name":"CDubai","kills":15,"deaths":16,"assists":4,"elo":1059},
            {"name":"ma1kyy","kills":12,"deaths":14,"assists":6,"elo":970},
            {"name":"InkLauD","kills":10,"deaths":13,"assists":2,"elo":1027},
        ],
        players_t=[
            {"name":"antilose32","kills":14,"deaths":20,"assists":2,"elo":1121},
            {"name":"StichDarling","kills":20,"deaths":18,"assists":4,"elo":1180},
            {"name":"metophobia","kills":10,"deaths":17,"assists":3,"elo":963},
            {"name":"Youkai","kills":13,"deaths":16,"assists":1,"elo":1017},
            {"name":"Бабка апатчи","kills":9,"deaths":15,"assists":2,"elo":910},
        ],
    )
    with open("preview_match.html","w",encoding="utf-8") as f: f.write(html3)
    print("✅ preview_match.html")

    print("\nОткрой эти HTML файлы в браузере — вот как будет выглядеть результат!")
    print("На сервере бота сделай: pip install playwright && playwright install --with-deps chromium")
    print("Затем замени card_generator.py на card_generator_html.py")
