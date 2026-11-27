from lukoji_engine import config
from lukoji_engine.geometry import Rect, anchor_box, central_crop, get_profile, list_profiles


def test_config_loads_and_palette_is_official():
    cfg = config.load_config()
    p = cfg.brand["palette"]
    assert (p["noir"], p["blanc"], p["fond_clair"]) == ("#0B0B0B", "#FFFFFF", "#F6F6F3")
    assert (p["jaune"], p["orange"], p["orange_intense"]) == ("#FFD23F", "#FF8A00", "#FF5A00")
    assert cfg.get("encode.video_codec") == "libx264"


def test_env_override(monkeypatch):
    monkeypatch.setenv("LUKOJI_ENCODE__CRF", "21")
    config.load_config.cache_clear()
    assert config.load_config().get("encode.crf") == 21


def test_rect_operations():
    a, b = Rect(0, 0, 100, 100), Rect(50, 50, 100, 100)
    assert a.intersect(b) == Rect(50, 50, 50, 50)
    assert a.intersects(b) and not a.intersects(Rect(100, 0, 10, 10))
    assert a.contains(Rect(10, 10, 20, 20)) and not a.contains(b)
    assert Rect.parse("1,2,3,4") == Rect(1, 2, 3, 4)


def test_central_crops():
    assert central_crop(1080, 1920, (4, 5)) == Rect(0, 285, 1080, 1350)
    assert central_crop(1080, 1920, (3, 4)) == Rect(0, 240, 1080, 1440)


def test_every_profile_resolves_with_positive_safe_zone():
    for name in list_profiles():
        p = get_profile(name)
        assert p.safe.w > 0 and p.safe.h > 0 and p.canvas.contains(p.safe), name


def test_platforms_have_distinct_safe_zones():
    zones = {get_profile(n).safe for n in ("tiktok", "instagram_reels", "facebook_reels", "youtube_shorts")}
    assert len(zones) == 4  # pas de coordonnées uniques supposées pour toutes les plateformes


def test_universal_is_intersection_of_members():
    u = get_profile("vertical_universal")
    for m in u.members:
        assert get_profile(m).safe.contains(u.safe)


def test_anchor_box_stays_inside_safe():
    p = get_profile("vertical_universal")
    for anchor in ("top_left", "top_right", "bottom_left", "bottom_right"):
        assert p.safe.contains(anchor_box(anchor, p.safe, 220, 60))


def test_youtube_reserved_zone_bottom_right():
    p = get_profile("youtube_16x9")
    assert p.reserved and anchor_box("bottom_right", p.safe, 240, 65).intersects(p.reserved[0])
