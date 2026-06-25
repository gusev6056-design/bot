"""
HTML-шаблоны карточек Actual FACEIT.
Используется из card_generator_html.py
"""
import base64
from typing import Optional


def _b64(img_bytes: Optional[bytes]) -> str:
    if not img_bytes:
        return ""
    return "data:image/png;base64," + base64.b64encode(img_bytes).decode()


def _hex_badge_svg(level: int, size: int = 44) -> str:
    import math
    colors = {
        1: "#787878", 2: "#32a028", 3: "#32a028", 4: "#32a028",
        5: "#dcb414", 6: "#dcb414", 7: "#dc6e14", 8: "#dc6e14",
        9: "#d22d1e", 10: "#d22d1e",
    }
    c = colors.get(level, "#787878")
    cx = cy = size / 2
    r = size / 2 - 2
    pts = " ".join(
        f"{cx + r * math.cos(math.radians(60 * i - 30)):.1f},"
        f"{cy + r * math.sin(math.radians(60 * i - 30)):.1f}"
        for i in range(6)
    )
    fs = max(size - 24, 9)
    return (
        f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
        f'<polygon points="{pts}" fill="{c}" stroke="rgba(255,255,255,.2)" stroke-width="1.5"/>'
        f'<text x="{cx}" y="{cy + fs // 3}" font-size="{fs}" font-weight="bold" '
        f'fill="white" text-anchor="middle" font-family="Arial,sans-serif">{level}</text>'
        f'</svg>'
    )


LEVEL_ELO = [0, 500, 750, 900, 1050, 1200, 1350, 1530, 1750, 2000, 9999]
LEVEL_COLORS = {
    1: "#787878", 2: "#32a028", 3: "#32a028", 4: "#32a028",
    5: "#dcb414", 6: "#dcb414", 7: "#dc6e14", 8: "#dc6e14",
    9: "#d22d1e", 10: "#d22d1e",
}


def faceit_level(elo: int) -> int:
    for i in range(10, 0, -1):
        if elo >= LEVEL_ELO[i - 1]:
            return i
    return 1


# Map name → (gradient_from, gradient_to, accent_color)
MAP_STYLES = {
    "rust":      ("#3d1a0a", "#5c2a10", "#c84a1e"),
    "sandstone": ("#2e2208", "#4a380e", "#c8961e"),
    "province":  ("#0a1e10", "#143020", "#1ec87a"),
    "zone 9":    ("#0a0e2a", "#101838", "#1e56c8"),
    "zone9":     ("#0a0e2a", "#101838", "#1e56c8"),
    "breeze":    ("#0a1e2e", "#10303e", "#1ea8c8"),
    "sakura":    ("#2a0e1e", "#3e1028", "#c81e6e"),
    "mirage":    ("#2e2208", "#4a3a10", "#c8aa1e"),
    "inferno":   ("#3a1008", "#581a10", "#e05020"),
    "dust2":     ("#2a1e0a", "#3e2e10", "#c8961e"),
    "nuke":      ("#0e1e10", "#16301a", "#32c850"),
    "overpass":  ("#0e1828", "#183040", "#3264c8"),
    "vertigo":   ("#1a0e2e", "#281440", "#7832c8"),
    "ancient":   ("#1e1208", "#30200e", "#c8781e"),
    "anubis":    ("#1a0e08", "#2e1a10", "#c8501e"),
    "train":     ("#101e10", "#183018", "#28c828"),
    "cache":     ("#0e1a10", "#162818", "#28b428"),
    "cobblestone":("#1e1a0e","#2e2814","#c8b41e"),
}

def _map_style(map_name: str):
    key = map_name.lower().strip()
    return MAP_STYLES.get(key, ("#1e1428", "#2a1c36", "#7846c8"))


BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', 'Arial', sans-serif;
  background: #0d0d12;
  color: #f0f0f5;
  -webkit-font-smoothing: antialiased;
}

:root {
  --bg:     #0d0d12;
  --panel:  #111118;
  --card:   #181824;
  --card2:  #1c1c2a;
  --border: rgba(140,120,220,.13);
  --red:    #e91e8c;
  --pink:   #e91e8c;
  --blue:   #4fc3f7;
  --green:  #2ecc71;
  --gray:   #7878a0;
  --gray2:  #1e1e30;
  --gold:   #d4af37;
  --silver: #9aa0bb;
  --bronze: #aa6c32;
}
"""

BLUE_LOCK_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', 'Arial', sans-serif;
  background: #f0f3ff;
  color: #0a0e1a;
  -webkit-font-smoothing: antialiased;
}

:root {
  --bg:     #f0f3ff;
  --panel:  #ffffff;
  --card:   #f5f7ff;
  --card2:  #e8ecfc;
  --border: rgba(0,71,255,.10);
  --red:    #e02020;
  --pink:   #0047ff;
  --green:  #00a854;
  --gray:   #6b7299;
  --gray2:  #c8d0f0;
  --gold:   #d4af37;
  --silver: #8899cc;
  --bronze: #aa6c32;
  --blue:   #0047ff;
  --blue2:  #003acc;
}

/* speed-line diagonal pattern */
.bl-pattern {
  background-image: repeating-linear-gradient(
    -60deg,
    transparent 0px, transparent 14px,
    rgba(0,71,255,.04) 14px, rgba(0,71,255,.04) 15px
  );
}

/* sharp corner bracket frame */
.bl-bracket::before,
.bl-bracket::after {
  content: '';
  position: absolute;
  width: 14px; height: 14px;
  border-color: #0047ff;
  border-style: solid;
}
.bl-bracket::before { top: -2px; left: -2px; border-width: 2px 0 0 2px; }
.bl-bracket::after  { bottom: -2px; right: -2px; border-width: 0 2px 2px 0; }
"""

def _frame_html(av_html: str, frame_style: str, level_color: str) -> str:
    """Wrap avatar in a decorative frame."""
    if frame_style == "blue_lock":
        return f"""
        <div style="position:relative;display:inline-block;padding:4px;">
          <div style="position:absolute;top:0;left:0;width:16px;height:16px;
                      border-top:3px solid #0047ff;border-left:3px solid #0047ff;"></div>
          <div style="position:absolute;top:0;right:0;width:16px;height:16px;
                      border-top:3px solid #0047ff;border-right:3px solid #0047ff;"></div>
          <div style="position:absolute;bottom:0;left:0;width:16px;height:16px;
                      border-bottom:3px solid #0047ff;border-left:3px solid #0047ff;"></div>
          <div style="position:absolute;bottom:0;right:0;width:16px;height:16px;
                      border-bottom:3px solid #0047ff;border-right:3px solid #0047ff;"></div>
          <div style="overflow:hidden;border-radius:6px;
                      clip-path:polygon(8px 0%,100% 0%,100% calc(100% - 8px),calc(100% - 8px) 100%,0% 100%,0% 8px);">
            {av_html}
          </div>
        </div>"""
    elif frame_style == "neon_blue":
        return f"""
        <div style="position:relative;display:inline-block;
                    border-radius:14px;
                    box-shadow:0 0 0 2px #0047ff, 0 0 12px #0047ff88, 0 0 28px #0047ff44;">
          <div style="border-radius:12px;overflow:hidden;">{av_html}</div>
        </div>"""
    elif frame_style == "gold":
        return f"""
        <div style="position:relative;display:inline-block;padding:3px;
                    background:linear-gradient(135deg,#d4af37,#f5e06e,#a07820,#d4af37);
                    border-radius:16px;">
          <div style="border-radius:13px;overflow:hidden;">{av_html}</div>
        </div>"""
    elif frame_style == "level":
        return f"""
        <div style="position:relative;display:inline-block;padding:3px;
                    background:linear-gradient(135deg,{level_color},{level_color}88);
                    border-radius:16px;box-shadow:0 0 16px {level_color}66;">
          <div style="border-radius:13px;overflow:hidden;">{av_html}</div>
        </div>"""
    else:
        return av_html


# ═══════════════════════════════════════════════════════════════
#  PROFILE CARD
# ═══════════════════════════════════════════════════════════════
# ── Таблица маппинга названий предметов из магазина → коды стилей ──────────────
_BANNER_MAP = {
    "Баннер Blue Lock": "blue_lock_white",
    "Баннер Gold":      "gold",
    "Баннер Diamond":   "diamond",
    "Баннер Elite":     "elite",
}
_FRAME_MAP = {
    "Рамка Blue Lock":  "blue_lock",
    "Рамка Gold":       "gold",
    "Рамка Diamond":    "neon_blue",
    "Рамка Elite":      "level",
}
_BG_MAP = {
    "Фон Blue Lock":    "blue_lock_white",
}

def profile_html(
    username="Unknown", game_id="", user_id=0, elo=1000,
    wins=0, losses=0, kills=0, deaths=0, assists=0,
    is_premium=False, is_admin=False, global_rank=0,
    league="default", map_stats=None, recent=None,
    leaderboard=None, mvp_count=0, is_verified=False,
    avatar_bytes=None, join_date="", playtime_hours=0,
    # ── Косметика (принимаем русские названия из магазина бота) ──
    active_frame=None,      # e.g. "Рамка Blue Lock"
    active_banner=None,     # e.g. "Баннер Blue Lock"
    active_background=None, # e.g. "Фон Blue Lock"
    # ── Или напрямую коды стилей (для ручного вызова) ──
    frame_style=None,
    banner_style=None,
    background_style=None,
    theme=None,
    **_kw,
) -> str:
    # Маппинг русских названий → коды
    if active_banner and not banner_style:
        banner_style = _BANNER_MAP.get(active_banner, "default")
    if active_frame and not frame_style:
        frame_style = _FRAME_MAP.get(active_frame, "default")
    if active_background and not background_style:
        background_style = _BG_MAP.get(active_background, "default")
    # defaults
    banner_style     = banner_style     or "default"
    frame_style      = frame_style      or "default"
    background_style = background_style or "default"
    # theme: blue_lock если любой Blue Lock косметик надет
    is_bl = (
        theme == "blue_lock"
        or banner_style == "blue_lock_white"
        or background_style == "blue_lock_white"
    )
    games   = wins + losses
    kd      = round(kills / max(deaths, 1), 2)
    wr      = round(wins / max(games, 1) * 100, 1)
    level   = faceit_level(elo)
    lv_clr  = LEVEL_COLORS.get(level, "#787878")
    avg_k   = round(kills / max(games, 1), 1)
    kpr     = round(kills / max(games, 1) / 15, 2)
    impact  = round(kd * 1.05, 2)
    svr     = round(wr / 100, 2)
    calibrated = games >= 5

    # --- avatar ---
    av_bg  = "#e8ecfc" if is_bl else "#26202360"
    av_bdr = "rgba(0,71,255,.2)" if is_bl else "rgba(255,255,255,.1)"
    person_fill = "#8899cc" if is_bl else "#4a4550"
    if avatar_bytes:
        av_src = _b64(avatar_bytes)
        _av_inner = (
            f'<img src="{av_src}" '
            f'style="width:100px;height:100px;border-radius:12px;object-fit:cover;">'
        )
    else:
        _av_inner = (
            f'<div style="width:100px;height:100px;border-radius:12px;'
            f'background:{av_bg};border:2px solid {av_bdr};'
            f'display:flex;align-items:center;justify-content:center;">'
            f'<svg width="52" height="52" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="26" cy="20" r="11" fill="{person_fill}"/>'
            f'<ellipse cx="26" cy="46" rx="18" ry="13" fill="{person_fill}"/>'
            f'</svg></div>'
        )
    av_html = _frame_html(_av_inner, frame_style, lv_clr)

    # --- badges (admin only — verified & premium move inline next to nick) ---
    badges = ""
    if is_admin:
        badges += '<span style="background:#1a1a42;color:#5865f2;border-radius:4px;padding:2px 7px;font-size:11px;">ADMIN</span>'

    # --- inline icons next to username ---
    inline_icons = ""
    if is_verified:
        inline_icons += '<span title="Верифицирован" style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#1a3a24;border:1.5px solid #2ecc71;font-size:13px;line-height:1;flex-shrink:0;">✓</span>'
    if is_premium:
        inline_icons += '<span title="Премиум" style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#3d2e00;border:1.5px solid #d4a000;font-size:12px;line-height:1;flex-shrink:0;">👑</span>'

    # --- KD arc ---
    kd_pct = min(kd / 3.0, 1.0)
    total_dash = 188.5
    kd_offset = int(total_dash * (1 - kd_pct))

    # --- calibration block ---
    cal_pct = min(int(games / 5 * 100), 100)
    cal_block = f"""
    <div style="flex:1;background:var(--card);border:1px solid var(--border);border-radius:10px;
                padding:12px 14px;position:relative;display:flex;flex-direction:column;justify-content:space-between;">
      <div>
        <div style="font-size:12px;color:var(--gray);margin-bottom:2px;">Level</div>
        {"" if calibrated else
         '<div style="position:absolute;right:12px;top:12px;width:32px;height:32px;border-radius:50%;'
         'background:var(--card2);border:1px solid var(--border);display:flex;align-items:center;'
         'justify-content:center;font-size:15px;">🔒</div>'}
        <div style="font-size:13px;font-weight:600;margin-top:6px;">{"" if calibrated else "Калибровка"}</div>
        <div style="font-size:22px;font-weight:800;color:var(--pink);">{level if calibrated else f"{games}/5"}<span style="font-size:14px;color:var(--gray);font-weight:400;">/10</span></div>
      </div>
      <div>
        <div style="background:var(--card2);border-radius:3px;height:5px;overflow:hidden;margin-top:8px;">
          <div style="height:5px;border-radius:3px;background:var(--pink);width:{elo//2000*100 if calibrated else cal_pct}%;"></div>
        </div>
        <div style="font-size:11px;color:var(--gray);margin-top:3px;">{"ELO " + str(elo) if calibrated else f"Сыграно {games} из 5"}</div>
      </div>
    </div>"""

    # --- 6 mini stat cards ---
    def mini(label, val, pct_raw, mx):
        p = min(pct_raw / max(mx, 0.001), 1.0)
        w = int(p * 100)
        tier = "High" if p >= 0.7 else ("Med" if p >= 0.4 else "Low")
        tc   = "#2ecc71" if tier == "High" else ("#f1c40f" if tier == "Med" else "#e91e8c")
        bc   = "#e91e8c"
        return f"""
        <div style="flex:1;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:10px 12px;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
            <span style="font-size:12px;color:var(--gray);">{label}</span>
            <span style="font-size:20px;font-weight:700;">{val}</span>
          </div>
          <div style="background:var(--card2);border-radius:3px;height:3px;overflow:hidden;">
            <div style="height:3px;border-radius:3px;background:{bc};width:{w}%;"></div>
          </div>
          <span style="font-size:10px;color:{tc};display:block;margin-top:3px;">{tier}</span>
        </div>"""

    stats_row1 = f"""
    <div style="display:flex;gap:6px;margin-bottom:6px;">
      {mini("Rating",  f"{kd:.2f}",  kd,    3.0)}
      {mini("AVG",     str(avg_k),   avg_k, 30.0)}
      {mini("Impact",  f"{impact:.2f}", impact, 3.0)}
    </div>"""
    stats_row2 = f"""
    <div style="display:flex;gap:6px;">
      {mini("KPR",     f"{kpr:.2f}", kpr,    1.0)}
      {mini("Assists", str(assists), assists, 200.0)}
      {mini("SVR",     f"{svr:.2f}", svr,    1.0)}
    </div>"""

    # --- map stats ---
    map_list = map_stats or []
    if map_list:
        best = max(map_list, key=lambda m: m.get("wins", 0) / max(m.get("wins", 0) + m.get("losses", 0), 1))
        bw = best.get("wins", 0)
        bl = best.get("losses", 0)
        bg = bw + bl
        bwr = round(bw / max(bg, 1) * 100)
        bkd = best.get("kd", 0.0)
        bmap = best.get("map", "?")

        total_g = sum((m.get("wins",0)+m.get("losses",0)) for m in map_list)
        total_w = sum(m.get("wins",0) for m in map_list)
        total_wr = round(total_w / max(total_g, 1) * 100)
        wr_deg = int(total_wr / 100 * 314.15)
        wr_rem = 314.15 - wr_deg
        wr_clr = "#2ecc71" if total_wr >= 50 else "#e91e8c"

        small_maps = ""
        for m in map_list[:6]:
            mn = m.get("map", "?")[:9]
            mw = m.get("wins", 0)
            ml = m.get("losses", 0)
            mg = mw + ml
            mwr = round(mw / max(mg, 1) * 100)
            mkd = m.get("kd", 0.0)
            mc = "#2ecc71" if mwr >= 50 else "#e91e8c"
            ms_from, ms_to, ms_acc = _map_style(mn)
            small_maps += f"""
            <div style="background:linear-gradient(135deg,{ms_from},{ms_to});border:1px solid {ms_acc}44;
                        border-radius:10px;padding:10px 8px;flex:1;min-width:120px;
                        border-left:3px solid {ms_acc};position:relative;overflow:hidden;">
              <div style="position:absolute;inset:0;background-image:repeating-linear-gradient(-45deg,transparent,transparent 8px,rgba(255,255,255,.03) 8px,rgba(255,255,255,.03) 9px);pointer-events:none;"></div>
              <div style="position:relative;z-index:1;">
                <div style="font-size:12px;font-weight:700;margin-bottom:5px;color:{ms_acc};">{mn}</div>
                <div style="font-size:11px;color:rgba(255,255,255,.6);margin-bottom:2px;">
                  <span style="color:#2ecc71;">W = {mw}</span> &nbsp; <span style="color:#e91e8c;">L = {ml}</span>
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,.5);">K/D = {mkd:.2f} &nbsp; W/R = <span style="color:{mc};">{mwr}%</span></div>
              </div>
            </div>"""

        map_section = f"""
        <div style="display:flex;gap:10px;margin-bottom:10px;">
          <!-- win rate donut -->
          <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;
                      padding:14px;display:flex;align-items:center;gap:14px;min-width:190px;">
            <svg width="80" height="80" viewBox="0 0 80 80">
              <circle cx="40" cy="40" r="34" fill="none" stroke="#1c1c2e" stroke-width="8"/>
              <circle cx="40" cy="40" r="34" fill="none" stroke="#4fc3f7" stroke-width="8"
                stroke-dasharray="{wr_rem:.1f} {wr_deg:.1f}"
                stroke-dashoffset="0" transform="rotate(-90 40 40)" stroke-linecap="round"/>
              <circle cx="40" cy="40" r="34" fill="none" stroke="#e91e8c" stroke-width="8"
                stroke-dasharray="{wr_deg:.1f} {wr_rem:.1f}"
                stroke-dashoffset="{wr_rem:.1f}" transform="rotate(-90 40 40)" stroke-linecap="round"/>
              <text x="40" y="36" text-anchor="middle" fill="#f0f0f2" font-size="14" font-weight="800" font-family="Arial">{total_wr}%</text>
              <text x="40" y="52" text-anchor="middle" fill="#7a7880" font-size="9" font-family="Arial">Win Rate</text>
            </svg>
            <div>
              <div style="font-size:12px;color:var(--gray);">W = <span style="color:#2ecc71;">{total_w}</span></div>
              <div style="font-size:12px;color:var(--gray);">L = <span style="color:#e91e8c;">{total_g - total_w}</span></div>
            </div>
          </div>

          <!-- best map -->
          <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;
                      padding:14px;flex:1;position:relative;overflow:hidden;">
            <div style="position:absolute;top:6px;right:8px;font-size:9px;color:var(--gray);
                        writing-mode:vertical-rl;letter-spacing:2px;font-weight:700;opacity:.5;">BEST MAP</div>
            <div style="font-size:12px;color:var(--gray);margin-bottom:4px;">Лучшая карта</div>
            <div style="font-size:20px;font-weight:800;">{bmap}</div>
            <div style="font-size:12px;color:var(--gray);margin-top:4px;">
              W = <span style="color:#2ecc71;">{bw}</span> &nbsp; L = <span style="color:#e91e8c;">{bl}</span>
            </div>
            <div style="font-size:12px;color:var(--gray);">K/D = {bkd:.2f} &nbsp;&nbsp; W/R = <span style="color:#2ecc71;">{bwr}%</span></div>
          </div>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:6px;">{small_maps}</div>"""
    else:
        cal_pct2 = min(int(games / 5 * 100), 100)
        map_section = f"""
        <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;
                    padding:24px;text-align:center;">
          <div style="font-size:28px;margin-bottom:10px;">🔒</div>
          <div style="font-size:15px;font-weight:700;margin-bottom:4px;">Статистика по картам</div>
          <div style="font-size:13px;color:var(--gray);margin-bottom:12px;">Доступна после калибровки</div>
          <div style="background:var(--card2);border-radius:3px;height:5px;max-width:200px;margin:0 auto 4px;">
            <div style="height:5px;border-radius:3px;background:var(--pink);width:{cal_pct2}%;"></div>
          </div>
          <span style="font-size:12px;color:var(--gray);">{games}/5 матчей</span>
        </div>"""

    # --- recent matches ---
    recent_list = recent or []
    recent_html = ""
    for ri in range(20):
        if ri < len(recent_list):
            item = recent_list[ri]
            won = item.get("won", False) if isinstance(item, dict) else bool(item)
            label = "W" if won else "L"
            bg = "#1a3a24" if won else "#3a1a1a"
            border = "#2ecc71" if won else "#e91e8c"
            color = "#2ecc71" if won else "#e91e8c"
            recent_html += (
                f'<div style="width:28px;height:28px;border-radius:5px;background:{bg};'
                f'border:1px solid {border};display:flex;align-items:center;justify-content:center;'
                f'font-size:10px;font-weight:700;color:{color};">{label}</div>'
            )
        else:
            recent_html += (
                '<div style="width:28px;height:28px;border-radius:5px;'
                'background:var(--card2);border:1px solid var(--border);"></div>'
            )

    # --- leaderboard places ---
    lb = leaderboard or []
    places_html = ""
    rank_colors = {1: "var(--gold)", 2: "var(--silver)", 3: "var(--bronze)"}
    for i, entry in enumerate(lb[:3], start=1):
        if isinstance(entry, dict):
            nm          = str(entry.get("name", "?"))[:14]
            av_bytes_lb = entry.get("avatar")
            elo_lb      = entry.get("elo", 0)
        elif isinstance(entry, (list, tuple)):
            # bot sends tuples serialised as JSON arrays: [rank, name, elo, ...]
            nm          = str(entry[1])[:14] if len(entry) > 1 else "?"
            elo_lb      = entry[2] if len(entry) > 2 else 0
            av_bytes_lb = None
        else:
            nm          = str(entry)[:14]
            elo_lb      = 0
            av_bytes_lb = None

        rc       = rank_colors.get(i, "var(--gray)")
        lv_lb    = faceit_level(int(elo_lb)) if elo_lb else 1
        lv_clr_lb = LEVEL_COLORS.get(lv_lb, "#787878")

        # avatar may arrive as base64 string (encoded by card_client)
        if isinstance(av_bytes_lb, str) and av_bytes_lb:
            try:
                av_bytes_lb = base64.b64decode(av_bytes_lb)
            except Exception:
                av_bytes_lb = None

        if av_bytes_lb:
            av_l = (f'<img src="{_b64(av_bytes_lb)}" style="width:24px;height:24px;'
                    f'border-radius:50%;object-fit:cover;border:1.5px solid {lv_clr_lb};">')
        else:
            av_l = (f'<div style="width:24px;height:24px;border-radius:50%;'
                    f'background:{lv_clr_lb}22;border:1.5px solid {lv_clr_lb};'
                    f'display:flex;align-items:center;justify-content:center;'
                    f'font-size:9px;font-weight:700;color:{lv_clr_lb};">{lv_lb}</div>')

        places_html += f"""
        <div style="display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid var(--border);">
          <span style="font-size:14px;font-weight:700;color:{rc};width:22px;">{i}.</span>
          {av_l}
          <span style="font-size:13px;flex:1;">{nm}</span>
        </div>"""
    if not calibrated:
        places_html += f"""
        <div style="display:flex;align-items:center;gap:8px;padding:5px 0;">
          <span style="font-size:12px;color:var(--gray);">–</span>
          <span style="font-size:12px;color:var(--gray);">Калибровка {games}/5</span>
        </div>"""
    if not places_html:
        places_html = '<div style="font-size:12px;color:var(--gray);padding:4px 0;">Нет данных</div>'

    lv_badge_big = _hex_badge_svg(level, 52)
    join_str = join_date or "—"
    pt_str = f"{playtime_hours}h" if playtime_hours else "—"

    # ── choose CSS & banner based on theme ──
    chosen_css = BLUE_LOCK_CSS if is_bl else BASE_CSS

    # ── badge helpers ──
    def _bl_badge(bg, fg, border, text):
        return f'<span style="background:{bg};color:{fg};border:1px solid {border};border-radius:4px;padding:2px 7px;font-size:11px;margin-right:5px;">{text}</span>'

    if banner_style == "blue_lock_white" or is_bl:
        # ── BLUE LOCK WHITE BANNER (по референсу: брызги, большой номер, BLUE LOCK лого) ──
        bl_badges = ""
        if is_admin: bl_badges += _bl_badge("#e8eaff","#0047ff","#0047ff30","ADMIN")
        bl_inline = ""
        if is_verified: bl_inline += '<span title="Верифицирован" style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#e0ffe8;border:1.5px solid #00a854;font-size:13px;line-height:1;flex-shrink:0;color:#00a854;">✓</span>'
        if is_premium:  bl_inline += '<span title="Премиум" style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#fff8e0;border:1.5px solid #d4a000;font-size:12px;line-height:1;flex-shrink:0;">👑</span>'
        header_html = f"""
<!-- ── BLUE LOCK WHITE BANNER ── -->
<div style="position:relative;overflow:hidden;min-height:148px;
            background:linear-gradient(110deg,#ffffff 0%,#f2f5ff 45%,#e8eeff 100%);
            border-bottom:3px solid #0047ff;">

  <!-- diagonal speed lines (аниме-линии скорости) -->
  <div style="position:absolute;inset:0;pointer-events:none;
    background-image:repeating-linear-gradient(-68deg,
      transparent,transparent 22px,rgba(0,71,255,.033) 22px,rgba(0,71,255,.033) 23px
    );"></div>

  <!-- левые брызги чернил -->
  <div style="position:absolute;left:0;top:0;bottom:0;width:110px;pointer-events:none;
    background:radial-gradient(ellipse 80% 120% at 0% 50%,rgba(0,71,255,.14) 0%,transparent 100%);"></div>
  <div style="position:absolute;left:0;top:-10px;width:80px;height:60px;pointer-events:none;
    background:radial-gradient(ellipse 60% 80% at 10% 30%,rgba(0,71,255,.10) 0%,transparent 100%);
    transform:rotate(-20deg);"></div>
  <div style="position:absolute;left:0;bottom:-10px;width:80px;height:60px;pointer-events:none;
    background:radial-gradient(ellipse 60% 80% at 10% 70%,rgba(0,71,255,.10) 0%,transparent 100%);
    transform:rotate(20deg);"></div>

  <!-- правые брызги + большая цифра уровня (как "8" на референсе) -->
  <div style="position:absolute;right:0;top:0;bottom:0;width:200px;pointer-events:none;
    background:radial-gradient(ellipse 100% 120% at 100% 50%,rgba(0,71,255,.12) 0%,transparent 100%);"></div>
  <div style="position:absolute;right:14px;top:50%;transform:translateY(-50%);
    font-size:148px;font-weight:900;line-height:1;letter-spacing:-6px;
    color:rgba(0,71,255,.09);user-select:none;pointer-events:none;font-style:italic;">{level}</div>

  <!-- BLUE LOCK логотип (правый низ) -->
  <div style="position:absolute;right:18px;bottom:10px;pointer-events:none;user-select:none;
    display:flex;align-items:center;gap:5px;">
    <svg width="16" height="16" viewBox="0 0 16 16">
      <circle cx="8" cy="8" r="7" fill="none" stroke="rgba(0,71,255,.35)" stroke-width="1.5"/>
      <circle cx="8" cy="8" r="3" fill="rgba(0,71,255,.35)"/>
    </svg>
    <span style="font-size:11px;font-weight:900;letter-spacing:2px;
      color:rgba(0,71,255,.35);font-style:italic;">BLUE LOCK</span>
  </div>

  <!-- левая синяя вертикальная полоса -->
  <div style="position:absolute;left:0;top:0;bottom:0;width:5px;background:#0047ff;"></div>

  <!-- контент -->
  <div style="position:relative;z-index:1;display:flex;align-items:center;gap:20px;padding:20px 160px 18px 24px;">
    {av_html}
    <div style="flex:1;">
      <div style="font-size:11px;color:#6b7299;font-weight:600;letter-spacing:.5px;margin-bottom:2px;">#: {game_id or user_id}</div>
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
        <div style="font-size:38px;font-weight:900;line-height:1;letter-spacing:-.5px;color:#0a0e1a;">{username}</div>
        {bl_inline}
      </div>
      <div style="font-size:12px;color:#6b7299;margin-top:3px;">ID: {user_id or game_id}</div>
      <div style="width:52px;height:3px;background:#0047ff;margin:8px 0 6px;border-radius:2px;"></div>
      <div style="display:flex;gap:4px;flex-wrap:wrap;">{bl_badges}</div>
    </div>
    <!-- ELO таблетка -->
    <div style="position:absolute;right:170px;top:50%;transform:translateY(-50%);text-align:center;">
      <div style="background:#0047ff;color:#fff;border-radius:10px;padding:8px 16px;">
        <div style="font-size:9px;font-weight:700;letter-spacing:1px;opacity:.8;margin-bottom:1px;">ELO</div>
        <div style="font-size:24px;font-weight:900;line-height:1;">{elo}</div>
      </div>
      <div style="font-size:10px;color:#6b7299;margin-top:4px;font-weight:600;">Lvl {level} · {league.capitalize()}</div>
    </div>
  </div>
</div>"""
    elif banner_style == "blue_lock_dark":
        header_html = f"""
<!-- ── BLUE LOCK DARK BANNER ── -->
<div style="position:relative;overflow:hidden;
            background:linear-gradient(135deg,#04091a 0%,#080f2e 60%,#030820 100%);
            padding:0;border-bottom:3px solid #0047ff;">
  <div style="position:absolute;inset:0;
    background-image:repeating-linear-gradient(-55deg,transparent,transparent 20px,rgba(0,71,255,.06) 20px,rgba(0,71,255,.06) 21px);
    pointer-events:none;"></div>
  <div style="position:absolute;left:0;top:0;bottom:0;width:5px;background:#0047ff;"></div>
  <div style="position:absolute;right:16px;top:50%;transform:translateY(-50%);
    font-size:80px;font-weight:900;letter-spacing:-3px;
    color:rgba(0,71,255,.08);line-height:1;pointer-events:none;user-select:none;white-space:nowrap;">
    ACTUAL<br>FACEIT
  </div>
  <div style="position:relative;z-index:1;display:flex;align-items:center;gap:20px;padding:20px 28px 18px 24px;">
    {av_html}
    <div>
      <div style="font-size:11px;color:#6b7299;font-weight:600;letter-spacing:.5px;margin-bottom:2px;">#: {game_id or user_id}</div>
      <div style="font-size:36px;font-weight:900;line-height:1.05;letter-spacing:-.5px;color:#f0f0f2;">{username}</div>
      <div style="font-size:12px;color:#6b7299;margin-top:2px;">ID: {user_id or game_id}</div>
      <div style="width:48px;height:3px;background:#0047ff;margin:8px 0;border-radius:2px;"></div>
      <div style="display:flex;gap:5px;">{badges}</div>
    </div>
    <div style="margin-left:auto;text-align:right;">
      <div style="background:#0047ff;color:#fff;border-radius:8px;padding:6px 14px;display:inline-block;margin-bottom:6px;">
        <div style="font-size:10px;font-weight:600;letter-spacing:.5px;opacity:.8;">ELO</div>
        <div style="font-size:22px;font-weight:900;line-height:1;">{elo}</div>
      </div>
      <div style="font-size:11px;color:#6b7299;">Lvl {level} · {league.capitalize()}</div>
    </div>
  </div>
</div>"""
    else:
        # ── DEFAULT DARK GAMING BANNER ──
        header_html = f"""
<!-- ── HEADER BANNER ── -->
<div style="position:relative;overflow:hidden;min-height:148px;
            background:linear-gradient(110deg,#0a0a14 0%,#0e0e1c 45%,#0b0b18 100%);
            border-bottom:2px solid #e91e8c;">
  <!-- diagonal texture -->
  <div style="position:absolute;inset:0;pointer-events:none;
    background-image:repeating-linear-gradient(-68deg,
      transparent,transparent 28px,rgba(233,30,140,.018) 28px,rgba(233,30,140,.018) 29px);"></div>
  <!-- pink glow left -->
  <div style="position:absolute;left:0;top:0;bottom:0;width:160px;pointer-events:none;
    background:radial-gradient(ellipse 90% 140% at 0% 50%,rgba(233,30,140,.10) 0%,transparent 100%);"></div>
  <!-- cyan glow right -->
  <div style="position:absolute;right:0;top:0;bottom:0;width:240px;pointer-events:none;
    background:radial-gradient(ellipse 100% 130% at 100% 50%,rgba(79,195,247,.06) 0%,transparent 100%);"></div>
  <!-- large faded ELO number -->
  <div style="position:absolute;right:14px;top:50%;transform:translateY(-50%);
    font-size:150px;font-weight:900;line-height:1;letter-spacing:-6px;
    color:rgba(233,30,140,.05);user-select:none;pointer-events:none;font-style:italic;">{elo}</div>
  <!-- left pink accent bar -->
  <div style="position:absolute;left:0;top:0;bottom:0;width:4px;
    background:linear-gradient(180deg,#4fc3f7,#e91e8c);"></div>
  <div style="position:relative;z-index:2;display:flex;align-items:center;gap:18px;padding:22px 175px 18px 22px;">
    {av_html}
    <div>
      <div style="font-size:11px;color:var(--gray);font-weight:600;letter-spacing:.5px;margin-bottom:2px;">#: {game_id or user_id}</div>
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
        <div style="font-size:36px;font-weight:900;line-height:1;letter-spacing:-.5px;color:#f0f0f5;">{username}</div>
        {inline_icons}
      </div>
      <div style="font-size:12px;color:var(--gray);margin-top:3px;">ID: {user_id or game_id}</div>
      <div style="width:52px;height:3px;background:linear-gradient(90deg,#4fc3f7,#e91e8c);margin:8px 0 6px;border-radius:2px;"></div>
      <div style="display:flex;gap:5px;flex-wrap:wrap;">{badges}</div>
    </div>
    <!-- ELO pill -->
    <div style="position:absolute;right:14px;top:50%;transform:translateY(-50%);text-align:center;z-index:3;">
      <div style="background:linear-gradient(135deg,#b5156c,#e91e8c);color:#fff;border-radius:10px;
                  padding:8px 18px;box-shadow:0 4px 18px rgba(233,30,140,.40);">
        <div style="font-size:9px;font-weight:700;letter-spacing:1px;opacity:.8;margin-bottom:1px;">ELO</div>
        <div style="font-size:24px;font-weight:900;line-height:1;">{elo}</div>
      </div>
      <div style="font-size:10px;color:var(--gray);margin-top:4px;font-weight:600;">Lvl {level} · {league.capitalize()}</div>
    </div>
  </div>
</div>"""

    # ── background wrapper CSS & open-tag ──
    if background_style == "blue_lock_white":
        bg_body_extra = "padding:8px; background:#c0d0ff;"
        bg_open  = """<div style="border-radius:6px;overflow:hidden;background:#f0f3ff;
  box-shadow:0 0 0 3px #0047ff, 0 0 0 6px #0047ff66, 0 0 0 9px #0047ff33,
             -3px -3px 0 8px #0047ff22, 3px 3px 0 8px #0047ff22,
             -6px 6px 0 5px #0047ff11, 6px -6px 0 5px #0047ff11;">"""
        bg_close = "</div>"
    elif background_style == "blue_lock_dark":
        bg_body_extra = "padding:8px; background:#001050;"
        bg_open  = '<div style="border-radius:6px;overflow:hidden;background:#080f2e;box-shadow:0 0 0 3px #0047ff, 0 0 0 7px #0047ff55, 0 0 24px #0047ff44;">'
        bg_close = "</div>"
    else:
        bg_body_extra = ""
        bg_open  = ""
        bg_close = ""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{chosen_css}
body {{ width:1060px; background:var(--bg); padding:0; {bg_body_extra} }}

.wf-watermark {{
  position:absolute;
  right:-10px; top:-20px;
  font-size:120px;
  font-weight:900;
  letter-spacing:-4px;
  color:rgba(255,255,255,.035);
  line-height:1;
  pointer-events:none;
  user-select:none;
  white-space:nowrap;
}}
</style>
</head>
<body>
{bg_open}
{header_html}

<!-- ── BODY ── -->
<div style="display:flex;gap:0;padding:14px;gap:12px;">

  <!-- LEFT COLUMN -->
  <div style="flex:1;display:flex;flex-direction:column;gap:12px;">

    <!-- STATISTIC -->
    <div style="background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:16px;box-shadow:0 2px 16px rgba(0,0,0,.35);">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <div style="width:4px;height:18px;background:#e91e8c;border-radius:2px;flex-shrink:0;"></div>
        <div style="font-size:15px;font-weight:700;color:#f0f0f5;">Statistic</div>
      </div>
      <div style="height:1px;background:var(--border);margin-bottom:12px;"></div>

      <!-- KD + Calibration -->
      <div style="display:flex;gap:8px;margin-bottom:8px;">
        <!-- KD Dial -->
        <div style="background:var(--card);border:1px solid var(--border);border-radius:10px;
                    padding:12px 14px;display:flex;align-items:center;gap:14px;min-width:210px;">
          <div style="position:relative;width:72px;height:72px;flex-shrink:0;">
            <svg width="72" height="72" viewBox="0 0 72 72" style="transform:rotate(-220deg);">
              <circle cx="36" cy="36" r="30" fill="none" stroke="#1c1c2e" stroke-width="7"
                stroke-dasharray="188.5" stroke-dashoffset="0" stroke-linecap="round"/>
              <circle cx="36" cy="36" r="30" fill="none"
                stroke="url(#kd_grad)" stroke-width="7"
                stroke-dasharray="188.5"
                stroke-dashoffset="{kd_offset}"
                stroke-linecap="round"/>
              <defs>
                <linearGradient id="kd_grad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stop-color="#4fc3f7"/>
                  <stop offset="100%" stop-color="#e91e8c"/>
                </linearGradient>
              </defs>
            </svg>
            <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
                        font-size:15px;font-weight:800;">{kd:.2f}</div>
            <div style="position:absolute;top:-2px;left:50%;transform:translateX(-50%);
                        width:8px;height:8px;border-radius:50%;background:#e91e8c;"></div>
          </div>
          <div>
            <div style="font-size:12px;color:var(--gray);margin-bottom:6px;">Kill/Deaths</div>
            <div style="font-size:15px;font-weight:700;">
              <span style="color:var(--gray);">K = </span><span style="color:#4fc3f7;">{kills}</span>
              &nbsp;&nbsp;
              <span style="color:var(--gray);">D = </span><span style="color:#e91e8c;">{deaths}</span>
            </div>
          </div>
        </div>
        {cal_block}
      </div>

      {stats_row1}
      {stats_row2}
    </div>

    <!-- MAP STATISTIC -->
    <div style="background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:16px;flex:1;box-shadow:0 2px 16px rgba(0,0,0,.35);">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <div style="width:4px;height:18px;background:#e91e8c;border-radius:2px;flex-shrink:0;"></div>
        <div style="font-size:15px;font-weight:700;color:#f0f0f5;">Map Statistic</div>
      </div>
      <div style="height:1px;background:var(--border);margin-bottom:12px;"></div>
      {map_section}
    </div>
  </div>

  <!-- RIGHT COLUMN -->
  <div style="width:310px;flex-shrink:0;display:flex;flex-direction:column;gap:12px;">

    <!-- Item slots -->
    <div style="background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:10px 14px;box-shadow:0 2px 16px rgba(0,0,0,.35);">
      <div style="display:flex;gap:6px;">
        {"".join('<div style="flex:1;height:44px;border-radius:8px;background:var(--card2);border:1px solid var(--border);"></div>' for _ in range(6))}
      </div>
    </div>

    <!-- Playtime / Join Date / Games / MVP -->
    <div style="background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:14px;box-shadow:0 2px 16px rgba(0,0,0,.35);">
      <div style="display:flex;gap:0;margin-bottom:10px;">
        <div style="flex:1;">
          <div style="font-size:12px;color:var(--gray);">⏱ Playtime</div>
          <div style="font-size:18px;font-weight:700;margin-top:2px;">{pt_str}</div>
        </div>
        <div style="flex:1;">
          <div style="font-size:12px;color:var(--gray);">📅 Join Date</div>
          <div style="font-size:15px;font-weight:700;margin-top:2px;">{join_str}</div>
        </div>
      </div>
      <div style="height:1px;background:var(--border);margin-bottom:10px;"></div>
      <div style="display:flex;gap:0;">
        <div style="flex:1;">
          <div style="font-size:12px;color:var(--gray);">🎮 Game</div>
          <div style="font-size:18px;font-weight:700;margin-top:2px;">{games}</div>
        </div>
        <div style="flex:1;">
          <div style="font-size:12px;color:var(--gray);">⭐ MVP</div>
          <div style="font-size:18px;font-weight:700;margin-top:2px;">{mvp_count}</div>
        </div>
      </div>
    </div>

    <!-- League & Places -->
    <div style="background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:14px;box-shadow:0 2px 16px rgba(0,0,0,.35);">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
        <div>
          <div style="font-size:12px;color:var(--gray);">League</div>
          <div style="font-size:22px;font-weight:800;margin-top:2px;">{league.capitalize()}</div>
        </div>
        {lv_badge_big}
      </div>
      <div style="height:1px;background:var(--border);margin-bottom:10px;"></div>
      <div style="font-size:12px;color:var(--gray);margin-bottom:6px;">Places</div>
      {places_html}
    </div>

    <!-- Recent Matches -->
    <div style="background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:14px;flex:1;box-shadow:0 2px 16px rgba(0,0,0,.35);">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
        <div style="width:4px;height:16px;background:#e91e8c;border-radius:2px;flex-shrink:0;"></div>
        <div style="font-size:14px;font-weight:700;color:#f0f0f5;">Recent Matches</div>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;">
        {recent_html}
      </div>
    </div>

    <!-- Branding -->
    <div style="text-align:right;padding:2px 2px 0;">
      <span style="font-size:12px;font-weight:900;color:rgba(233,30,140,.30);letter-spacing:1px;">ACTUAL FACEIT</span>
    </div>

  </div>
</div>
{bg_close}
</body></html>"""


# ═══════════════════════════════════════════════════════════════
#  LEADERBOARD HTML
# ═══════════════════════════════════════════════════════════════
def leaderboard_html(players: list, title: str = "ЛУЧШИЕ ИГРОКИ", avatars: dict = None) -> str:
    avatars = avatars or {}
    words = title.upper().replace("📊", "").strip().split(" — ")[0].strip().split()
    w1 = words[0] if words else "ЛУЧШИЕ"
    w2 = " ".join(words[1:]) if len(words) > 1 else "ИГРОКИ"
    league_name = title.split(" — ")[-1].strip() if " — " in title else "Default"

    rank_bgs = {1: "rgba(70,55,10,.45)", 2: "rgba(50,50,60,.45)", 3: "rgba(60,38,14,.45)"}
    rows_html = ""
    for i, p in enumerate(players[:10]):
        rank = p.get("rank", i + 1)
        name = p.get("name", "Unknown")[:18]
        elo_p = p.get("elo", 1000)
        wins_p = p.get("wins", 0)
        losses_p = p.get("losses", 0)
        kd_p = p.get("kd", round(p.get("kills", 0) / max(p.get("deaths", 1), 1), 2))
        level_p = p.get("level", faceit_level(elo_p))
        uid = p.get("uid", 0)
        premium = p.get("is_premium", False)
        admin = p.get("is_admin", False)
        verified = p.get("is_verified", False)
        gm = wins_p + losses_p
        wr = round(wins_p / max(gm, 1) * 100)
        avg = round(p.get("kills", 0) / max(gm, 1))
        lv_clr = LEVEL_COLORS.get(level_p, "#787878")
        rank_clr = {1: "var(--gold)", 2: "var(--silver)", 3: "var(--bronze)"}.get(rank, "var(--gray)")
        row_bg = rank_bgs.get(rank, "transparent" if i % 2 == 0 else "rgba(24,20,22,.6)")
        wr_clr = "#2ecc71" if wr >= 60 else ("#f1c40f" if wr >= 50 else "#e91e8c")
        kd_clr = "#2ecc71" if kd_p >= 1.0 else "#e91e8c"

        av_bytes = avatars.get(uid)
        if av_bytes:
            av_html = f'<img src="{_b64(av_bytes)}" style="width:52px;height:52px;border-radius:8px;object-fit:cover;border:2px solid {lv_clr};">'
        else:
            av_html = f'<div style="width:52px;height:52px;border-radius:8px;background:#26202360;border:2px solid {lv_clr};display:flex;align-items:center;justify-content:center;font-size:18px;">👤</div>'

        badges_b = ""
        if verified: badges_b += '<span style="background:#1a3a24;color:#2ecc71;border-radius:3px;padding:1px 5px;font-size:10px;margin-right:3px;">✓</span>'
        if premium:  badges_b += '<span style="background:#3d2e00;color:#f1c40f;border-radius:3px;padding:1px 5px;font-size:10px;margin-right:3px;">PRO</span>'
        if admin:    badges_b += '<span style="background:#1a1a42;color:#5865f2;border-radius:3px;padding:1px 5px;font-size:10px;">ADM</span>'

        lv_badge = _hex_badge_svg(level_p, 32)

        rows_html += f"""
        <tr style="background:{row_bg};">
          <td style="padding:10px 16px;font-size:26px;font-weight:900;color:{rank_clr};width:56px;">{rank}</td>
          <td style="padding:8px 8px;width:60px;">{av_html}</td>
          <td style="padding:8px 0;">
            <div style="background:linear-gradient(90deg,{lv_clr}18 0%,transparent 100%);
                        border-left:3px solid {lv_clr};padding:6px 12px;border-radius:0 6px 6px 0;">
              <div style="font-size:11px;color:var(--gray);">#{uid if uid else "—"}</div>
              <div style="font-size:16px;font-weight:700;">{name}</div>
              <div style="display:flex;gap:3px;margin-top:2px;">{badges_b}</div>
            </div>
          </td>
          <td style="padding:8px 14px;width:100px;">
            <div style="font-size:11px;color:var(--gray);"><span style="color:#2ecc71;">W{wins_p}</span> <span style="color:#e91e8c;">L{losses_p}</span></div>
            <div style="font-size:18px;font-weight:700;">{gm}</div>
          </td>
          <td style="padding:8px 14px;width:76px;font-size:18px;font-weight:700;color:{wr_clr};">{wr}%</td>
          <td style="padding:8px 10px;width:100px;">
            <div style="display:flex;align-items:center;gap:5px;">{lv_badge}<span style="font-size:16px;font-weight:700;color:{lv_clr};">{elo_p}</span></div>
          </td>
          <td style="padding:8px 14px;width:76px;font-size:18px;font-weight:700;color:{kd_clr};">{kd_p:.2f}</td>
          <td style="padding:8px 14px;width:60px;font-size:16px;font-weight:700;">{avg}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{BASE_CSS}
body {{ width:1080px; background:var(--bg); padding:0; }}
.lb-header {{
  position:relative;padding:24px 32px 20px;overflow:hidden;
  background:linear-gradient(135deg,#0d0d14 0%,#0e0916 60%,#0d0d18 100%);
}}
.lb-header::before {{
  content:'';position:absolute;inset:0;
  background-image:repeating-linear-gradient(-45deg,transparent,transparent 22px,rgba(255,255,255,.022) 22px,rgba(255,255,255,.022) 23px);
}}
table {{ width:100%;border-collapse:collapse; }}
thead th {{ padding:8px 14px;font-size:12px;font-weight:500;color:var(--gray);text-align:left;border-bottom:1px solid var(--card2); }}
tbody tr {{ border-bottom:1px solid var(--card2); }}
</style></head>
<body>
<div class="lb-header">
  <div style="position:relative;z-index:1;">
    <div style="font-size:54px;font-weight:900;line-height:1;letter-spacing:-1px;margin-bottom:14px;">
      <span style="color:#e91e8c;">{w1}</span> <span style="color:#f0f0f2;">{w2}</span>
    </div>
    <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.1);border-radius:10px;
                padding:5px 14px;display:inline-flex;align-items:center;gap:7px;">
      <span style="font-size:14px;font-weight:600;">{league_name}</span>
    </div>
  </div>
  <div style="position:absolute;right:24px;top:24px;z-index:1;font-size:13px;color:var(--gray);font-weight:600;">⚡ ACTUAL FACEIT</div>
</div>
<table>
  <thead>
    <tr>
      <th>Place</th><th colspan="2">Player</th><th>Games</th><th>Winrate</th><th>Points</th><th>K/D</th><th>AVG</th>
    </tr>
  </thead>
  <tbody>{rows_html}</tbody>
</table>
<div style="text-align:right;padding:8px 16px;font-size:11px;color:var(--gray2);">Actual Faceit Bot</div>
</body></html>"""


# ═══════════════════════════════════════════════════════════════
#  MATCH RESULT HTML
# ═══════════════════════════════════════════════════════════════
def match_result_html(
    match_code="", map_name="", winner="ct",
    score_w=0, score_l=0,
    players_ct=None, players_t=None,
    league="Default", avatars=None,
    server="Moscow",
) -> str:
    players_ct = players_ct or []
    players_t  = players_t  or []
    avatars    = avatars or {}
    ct_win     = winner.lower() in ("ct", "ct_win", "ct_side")

    sc_ct = score_w if ct_win else score_l
    sc_t  = score_l if ct_win else score_w
    total_rounds = sc_ct + sc_t

    # ─ find match MVP ─
    all_players = [("ct", p) for p in players_ct] + [("t", p) for p in players_t]
    mvp = max(all_players, key=lambda x: (
        x[1].get("kills", 0) / max(x[1].get("deaths", 1), 1)
    ), default=None)
    mvp_name  = mvp[1].get("name", mvp[1].get("username", "?")) if mvp else "?"
    mvp_level = faceit_level(mvp[1].get("elo", 1000)) if mvp else 1
    mvp_kd    = round(mvp[1].get("kills", 0) / max(mvp[1].get("deaths", 1), 1), 2) if mvp else 0
    mvp_imp   = round(mvp_kd * 0.9, 2) if mvp else 0
    mvp_rating= round(mvp_kd * 1.0, 2) if mvp else 0

    def player_row(p, side_is_ct, row_idx):
        pname  = p.get("name", p.get("username", "?"))[:14]
        pk     = p.get("kills", 0)
        pd     = p.get("deaths", 0)
        pa     = p.get("assists", 0)
        pelo   = p.get("elo", 1000)
        plv    = faceit_level(pelo)
        pkd    = round(pk / max(pd, 1), 2)
        pimp   = round(pkd * 0.9, 2)
        prat   = round(pkd * 1.0, 2)
        lv_c   = LEVEL_COLORS.get(plv, "#787878")
        lv_b   = _hex_badge_svg(plv, 26)
        kd_c   = "#2ecc71" if pkd >= 1.0 else "#e91e8c"
        uid    = p.get("uid", p.get("user_id", row_idx))
        av_b   = avatars.get(uid)
        elo_delta = p.get("elo_delta", 0)
        delta_str = ""
        if elo_delta:
            dc = "#2ecc71" if elo_delta > 0 else "#e91e8c"
            delta_str = f'<span style="font-size:9px;color:{dc};display:block;">{"+" if elo_delta>0 else ""}{elo_delta}</span>'

        if av_b:
            av_html = f'<img src="{_b64(av_b)}" style="width:36px;height:36px;border-radius:6px;object-fit:cover;border:1.5px solid {lv_c};">'
        else:
            av_html = (
                f'<div style="width:36px;height:36px;border-radius:6px;'
                f'background:linear-gradient(135deg,{lv_c}33,{lv_c}11);'
                f'border:1.5px solid {lv_c};display:flex;align-items:center;'
                f'justify-content:center;">{lv_b}</div>'
            )

        row_bg = "rgba(255,255,255,.025)" if row_idx % 2 == 0 else "transparent"

        if side_is_ct:
            return f"""
            <tr style="background:{row_bg};border-bottom:1px solid rgba(255,255,255,.05);">
              <td style="padding:7px 10px 7px 14px;">
                <div style="display:flex;align-items:center;gap:8px;">
                  {av_html}
                  <div>
                    <div style="font-size:13px;font-weight:700;">{pname}</div>
                    {delta_str}
                  </div>
                </div>
              </td>
              <td style="padding:7px 8px;text-align:center;font-size:14px;font-weight:700;">{pk}</td>
              <td style="padding:7px 8px;text-align:center;font-size:14px;color:#e91e8c;">{pd}</td>
              <td style="padding:7px 8px;text-align:center;font-size:13px;color:var(--gray);">{pkd:.2f}</td>
              <td style="padding:7px 8px;text-align:center;font-size:13px;color:var(--gray);">{pimp:.2f}</td>
              <td style="padding:7px 14px 7px 8px;text-align:center;font-size:14px;font-weight:700;color:{kd_c};">{prat:.2f}</td>
            </tr>"""
        else:
            return f"""
            <tr style="background:{row_bg};border-bottom:1px solid rgba(255,255,255,.05);">
              <td style="padding:7px 14px 7px 8px;text-align:center;font-size:14px;font-weight:700;color:{kd_c};">{prat:.2f}</td>
              <td style="padding:7px 8px;text-align:center;font-size:13px;color:var(--gray);">{pimp:.2f}</td>
              <td style="padding:7px 8px;text-align:center;font-size:13px;color:var(--gray);">{pkd:.2f}</td>
              <td style="padding:7px 8px;text-align:center;font-size:14px;color:#e91e8c;">{pd}</td>
              <td style="padding:7px 8px;text-align:center;font-size:14px;font-weight:700;">{pk}</td>
              <td style="padding:7px 10px 7px 8px;">
                <div style="display:flex;align-items:center;gap:8px;justify-content:flex-end;">
                  <div style="text-align:right;">
                    <div style="font-size:13px;font-weight:700;">{pname}</div>
                    {delta_str}
                  </div>
                  {av_html}
                </div>
              </td>
            </tr>"""

    ct_rows = "".join(player_row(p, True,  i) for i, p in enumerate(players_ct[:5]))
    t_rows  = "".join(player_row(p, False, i) for i, p in enumerate(players_t[:5]))

    ct_border = "#2ecc71" if ct_win else "#e91e8c"
    t_border  = "#e91e8c" if ct_win else "#2ecc71"
    ct_label  = "COUNTER TERRORISTS"
    t_label   = "TERRORISTS"
    ct_tag    = "✓ ПОБЕДА" if ct_win else ""
    t_tag     = "✓ ПОБЕДА" if not ct_win else ""
    ct_tag_clr= "#2ecc71" if ct_win else ""
    t_tag_clr = "#2ecc71" if not ct_win else ""

    ct_sc_clr = "#f0f0f2"
    t_sc_clr  = "#f0f0f2"

    match_title = f"DEFAULT #{match_code}" if match_code else "РЕЗУЛЬТАТ МАТЧА"

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{BASE_CSS}
body {{ width:1060px; background:var(--bg); padding:0; }}

/* diagonal pattern bg */
.bg-pattern {{
  position:absolute;inset:0;pointer-events:none;
  background-image:repeating-linear-gradient(
    -45deg, transparent, transparent 18px,
    rgba(255,255,255,.018) 18px, rgba(255,255,255,.018) 19px
  );
}}

.col-header {{
  font-size:10px;font-weight:600;letter-spacing:.5px;color:var(--gray);
  text-align:center;padding:5px 6px;
}}
.team-header {{
  display:flex;align-items:center;justify-content:space-between;
  padding:10px 14px;
}}
</style>
</head>
<body>

<!-- ─── TOP HEADER ─── -->
<div style="position:relative;overflow:hidden;background:linear-gradient(135deg,#1a0e12 0%,#111013 60%,#150f14 100%);
            padding:12px 18px;border-bottom:2px solid rgba(255,255,255,.06);">
  <div class="bg-pattern"></div>
  <div style="position:relative;z-index:1;display:flex;align-items:center;gap:0;">

    <!-- Match title -->
    <div style="flex:0 0 auto;min-width:200px;">
      <div style="font-size:20px;font-weight:900;letter-spacing:-.3px;">{match_title}</div>
    </div>

    <!-- Server + Map pills -->
    <div style="display:flex;gap:8px;align-items:center;flex:1;justify-content:center;">
      <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.1);border-radius:8px;
                  padding:5px 12px;display:flex;align-items:center;gap:7px;">
        <span style="font-size:10px;color:var(--gray);font-weight:600;">🌐 Сервер</span>
        <span style="font-size:13px;font-weight:700;">{server}</span>
      </div>
      <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.1);border-radius:8px;
                  padding:5px 12px;display:flex;align-items:center;gap:7px;">
        <span style="font-size:10px;color:var(--gray);font-weight:600;">🗺 Карта</span>
        <span style="font-size:13px;font-weight:700;">{map_name or "—"}</span>
      </div>
      <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.1);border-radius:8px;
                  padding:5px 12px;display:flex;align-items:center;gap:7px;">
        <span style="font-size:13px;font-weight:700;">{league}</span>
      </div>
    </div>

    <!-- Branding -->
    <div style="flex:0 0 auto;text-align:right;min-width:120px;">
      <div style="font-size:11px;font-weight:900;letter-spacing:.5px;color:rgba(255,255,255,.55);">ACTUAL</div>
      <div style="font-size:11px;font-weight:900;letter-spacing:.5px;color:rgba(255,255,255,.55);">FACEIT</div>
    </div>
  </div>
</div>

<!-- ─── SCORE BAR ─── -->
<div style="display:flex;align-items:center;background:#181416;border-bottom:1px solid rgba(255,255,255,.06);padding:0;">

  <!-- CT side label -->
  <div class="team-header" style="flex:1;border-right:1px solid rgba(255,255,255,.06);">
    <div style="display:flex;align-items:center;gap:8px;">
      <div style="width:3px;height:18px;background:{ct_border};border-radius:2px;"></div>
      <span style="font-size:12px;font-weight:700;letter-spacing:.5px;color:{"#e0e0e0"};">{ct_label}</span>
    </div>
    {"<span style='font-size:11px;font-weight:700;color:" + ct_tag_clr + ";'>" + ct_tag + "</span>" if ct_tag else ""}
  </div>

  <!-- Central score -->
  <div style="text-align:center;padding:10px 28px;flex-shrink:0;">
    <div style="font-size:10px;color:var(--gray);font-weight:600;letter-spacing:1px;margin-bottom:2px;">SCORE</div>
    <div style="font-size:32px;font-weight:900;line-height:1;letter-spacing:-1px;">
      <span style="color:{ct_border};">{sc_ct}</span>
      <span style="color:var(--gray);margin:0 6px;">:</span>
      <span style="color:{t_border};">{sc_t}</span>
    </div>
  </div>

  <!-- T side label -->
  <div class="team-header" style="flex:1;border-left:1px solid rgba(255,255,255,.06);justify-content:flex-end;">
    {"<span style='font-size:11px;font-weight:700;color:" + t_tag_clr + ";'>" + t_tag + "</span>" if t_tag else ""}
    <div style="display:flex;align-items:center;gap:8px;">
      <span style="font-size:12px;font-weight:700;letter-spacing:.5px;color:#e0e0e0;">{t_label}</span>
      <div style="width:3px;height:18px;background:{t_border};border-radius:2px;"></div>
    </div>
  </div>
</div>

<!-- ─── COLUMN HEADERS ─── -->
<div style="display:flex;background:#141214;border-bottom:1px solid rgba(255,255,255,.05);">
  <!-- CT headers -->
  <div style="flex:1;display:flex;">
    <div style="flex:2;padding:5px 14px;font-size:10px;font-weight:600;color:var(--gray);letter-spacing:.5px;">PLAYER</div>
    <div class="col-header" style="width:46px;">K</div>
    <div class="col-header" style="width:46px;">D</div>
    <div class="col-header" style="width:52px;">K/D</div>
    <div class="col-header" style="width:52px;">IMP</div>
    <div class="col-header" style="width:60px;">RATING</div>
  </div>
  <!-- Gap -->
  <div style="width:1px;background:rgba(255,255,255,.06);"></div>
  <!-- T headers (mirrored) -->
  <div style="flex:1;display:flex;">
    <div class="col-header" style="width:60px;">RATING</div>
    <div class="col-header" style="width:52px;">IMP</div>
    <div class="col-header" style="width:52px;">K/D</div>
    <div class="col-header" style="width:46px;">D</div>
    <div class="col-header" style="width:46px;">K</div>
    <div style="flex:2;padding:5px 14px;font-size:10px;font-weight:600;color:var(--gray);letter-spacing:.5px;text-align:right;">PLAYER</div>
  </div>
</div>

<!-- ─── PLAYER ROWS ─── -->
<div style="display:flex;background:var(--panel);">

  <!-- CT table -->
  <div style="flex:1;border-right:1px solid rgba(255,255,255,.06);">
    <table style="width:100%;border-collapse:collapse;">
      <colgroup>
        <col style="width:auto">
        <col style="width:46px">
        <col style="width:46px">
        <col style="width:52px">
        <col style="width:52px">
        <col style="width:60px">
      </colgroup>
      <tbody>{ct_rows}</tbody>
    </table>
  </div>

  <!-- T table -->
  <div style="flex:1;">
    <table style="width:100%;border-collapse:collapse;">
      <colgroup>
        <col style="width:60px">
        <col style="width:52px">
        <col style="width:52px">
        <col style="width:46px">
        <col style="width:46px">
        <col style="width:auto">
      </colgroup>
      <tbody>{t_rows}</tbody>
    </table>
  </div>
</div>

<!-- ─── BOTTOM: MAP INFO + MVP ─── -->
<div style="display:flex;gap:0;border-top:1px solid rgba(255,255,255,.06);background:#141214;">

  <!-- Map preview + info -->
  <div style="display:flex;align-items:center;gap:0;flex:1;border-right:1px solid rgba(255,255,255,.06);">
    <div style="width:110px;height:62px;background:linear-gradient(135deg,{_map_style(map_name)[0]},{_map_style(map_name)[1]});
                display:flex;align-items:center;justify-content:center;flex-shrink:0;
                border-right:3px solid {_map_style(map_name)[2]};position:relative;overflow:hidden;">
      <div style="position:absolute;inset:0;background-image:repeating-linear-gradient(-45deg,transparent,transparent 8px,rgba(255,255,255,.04) 8px,rgba(255,255,255,.04) 9px);"></div>
      <div style="position:relative;z-index:1;text-align:center;">
        <div style="font-size:11px;font-weight:800;color:{_map_style(map_name)[2]};letter-spacing:.5px;text-transform:uppercase;">{map_name or "MAP"}</div>
      </div>
    </div>
    <div style="padding:8px 14px;">
      <div style="font-size:10px;color:var(--gray);font-weight:600;letter-spacing:.5px;margin-bottom:2px;">PICKED MAP</div>
      <div style="font-size:16px;font-weight:800;">{map_name or "—"}</div>
    </div>
  </div>

  <!-- MVP -->
  <div style="flex:1;display:flex;align-items:center;gap:12px;padding:10px 16px;">
    <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#d4af37,#a08020);
                display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:900;color:#0f0d0e;flex-shrink:0;">
      {mvp_level}
    </div>
    <div style="flex:1;">
      <div style="font-size:10px;color:var(--gray);font-weight:600;letter-spacing:.5px;margin-bottom:1px;">GAME MVP</div>
      <div style="font-size:16px;font-weight:800;">{mvp_name}</div>
    </div>
    <div style="display:flex;gap:16px;">
      <div style="text-align:center;">
        <div style="font-size:10px;color:var(--gray);font-weight:600;margin-bottom:1px;">RATING</div>
        <div style="font-size:18px;font-weight:800;color:#d4af37;">{mvp_rating:.2f}</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:10px;color:var(--gray);font-weight:600;margin-bottom:1px;">K/D</div>
        <div style="font-size:18px;font-weight:800;color:#d4af37;">{mvp_kd:.2f}</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:10px;color:var(--gray);font-weight:600;margin-bottom:1px;">IMP</div>
        <div style="font-size:18px;font-weight:800;color:#d4af37;">{mvp_imp:.2f}</div>
      </div>
    </div>
  </div>

</div>

</body></html>"""
