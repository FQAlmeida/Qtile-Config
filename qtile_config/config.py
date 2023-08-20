import subprocess
from libqtile import widget, bar
from libqtile.layout.columns import Columns
from libqtile.layout.max import Max
from libqtile.layout.floating import Floating
from libqtile.layout.xmonad import MonadTall, MonadThreeCol
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger

from qtile_extras.widget.decorations import BorderDecoration
from fontawesome import icons

mod = "mod4"
terminal = guess_terminal()

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer -D pulse sset Master 5%-"),
        desc="Lower Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer -D pulse sset Master 5%+"),
        desc="Raise Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("amixer -D pulse sset Master 1+ toggle"),
        desc="Mute/Unmute Volume",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause player",
    ),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
]
groups = [Group(str(i)) for i in range(1, 5)]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )


colors = [
    ["#000000.0", "#ffffff.0"],
    ["#000000", "#000000"],
    ["#ffffff", "#ffffff"],
    ["#c60cfa", "#c60cfa"],
    ["#740bde", "#740bde"],
    ["#3900f5", "#3900f5"],
    ["#0b12de", "#0b12de"],
    ["#0c54fa", "#0c54fa"],
]

layout_theme = {
    "border_width": 1,
    "border_focus": ["#3900f5", "#3900f5"],
    "border_normal": ["#0b12de", "#0b12de"],
}


layouts = [
    MonadTall(**layout_theme, margin=5, single_border_width=0, single_margin=0),
    Max(border_width=0, margin=0),
    Columns(**layout_theme, margin=5, margin_on_single=0),
    MonadThreeCol(**layout_theme, margin=3, single_border_width=0, single_margin=0),
]


widget_defaults = dict(
    font="FiraCode Nerd Font,NotoSans Nerd Font,Ubuntu Mono,sans",
    fontsize=12,
    padding=0,
    background=colors[1],
)
extension_defaults = widget_defaults.copy()

widgets = [
    # widget.WindowName(),
    widget.Spacer(length=10),
    widget.GenPollText(
        update_interval=300,
        func=lambda: subprocess.check_output(
            "printf $(whoami)", shell=True, text=True
        ).upper(),
        foreground=colors[4],
        fmt=icons["heart"] + "  {}",
        decorations=[
            BorderDecoration(
                colour=colors[4],
                border_width=[0, 0, 2, 0],
            )
        ],
    ),
    widget.Spacer(length=5),
    # widget.WindowName(max_chars=25),
    widget.Spacer(length=5),
    widget.Prompt(foreground=colors[2], prompt="Run: "),
    widget.Spacer(),
    widget.Clock(
        format="%H:%M:%S %d/%m/%Y",
    ),
    widget.Spacer(),
    widget.CurrentLayoutIcon(
        foreground=colors[2],
        padding=0,
        scale=0.7,
    ),
    widget.CurrentLayout(foreground=colors[2], padding=5),
    widget.GroupBox(
        fontsize=11,
        margin_y=3,
        margin_x=4,
        padding_y=2,
        padding_x=3,
        borderwidth=3,
        active=colors[2],
        inactive=colors[4],
        rounded=False,
        highlight_color=colors[4],
        highlight_method="box",
        this_current_screen_border=colors[5],
        this_screen_border=colors[6],
        other_current_screen_border=colors[5],
        other_screen_border=colors[6],
    ),
    widget.Spacer(length=10),
    widget.PulseVolume(
        foreground=colors[2],
        fmt=icons["volume-up"] + "  {}",
        decorations=[
            BorderDecoration(
                colour=colors[4],
                border_width=[0, 0, 2, 0],
            )
        ],
    ),
    widget.Spacer(length=10),
    widget.WidgetBox(
        widgets=[
            widget.CPUGraph(),
            widget.MemoryGraph(),
            # widget.Systray(),
        ],
        text_closed=icons["arrow-circle-left"],
        text_open=icons["arrow-circle-right"],
        padding=5,
        close_button_location="right",
    ),
    widget.Spacer(length=5),
    widget.QuickExit(
        default_text=icons["power-off"],
        countdown_format=icons["chevron-left"] + "{}" + icons["chevron-right"],
        padding=10,
    ),
    widget.Spacer(length=10),
]

screens = [
    Screen(
        wallpaper="~/.config/qtile/wallpapers/beach-gray.jpg",
        wallpaper_mode="stretch",
        top=bar.Bar(
            background="#00000000",
            border_width=[0, 0, 0, 0],
            opacity=1,
            widgets=widgets,
            size=26,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

logger.info("Up and Running")
