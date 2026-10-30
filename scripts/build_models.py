#!/usr/bin/env python3
"""Convert the release OBJ/STL sources into the clean STL set in models/,
and render a preview PNG of each part into images/.

Usage: python3 scripts/build_models.py <release_files_dir>
Requires: numpy, matplotlib.
"""
import struct
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# source filename (in release_files) -> output name
PARTS = {
    "LisaMouseLogiechM185_base_v5.obj": "base",
    "LisaMouseLogiechM185_top_shell_v4.obj": "top_shell",
    "LisaMouseLogiechM185_top_shell_v4_Lisa_logo.obj": "top_shell_lisa_logo",
    "LisaMouseLogiechM185_left_button.obj": "left_button",
    "LisaMouseLogiechM185_right_button.obj": "right_button",
    "LisaMouseLogiechM185_v3_button_stop.obj": "button_stop",
    "LisaMouseLogiechM185_on-off_button.stl": "on_off_button",
    "LisaMouseLogiechM185_Battery_cover_1.stl.stl": "battery_cover_1",
    "LisaMouseLogiechM185_Battery_cover_2.stl.stl": "battery_cover_2",
}


def load_obj(path):
    verts, tris = [], []
    for line in open(path):
        if line.startswith("v "):
            verts.append([float(x) for x in line.split()[1:4]])
        elif line.startswith("f "):
            idx = [int(t.split("/")[0]) - 1 for t in line.split()[1:]]
            for i in range(1, len(idx) - 1):
                tris.append((idx[0], idx[i], idx[i + 1]))
    v = np.array(verts)
    return v[np.array(tris)]


def load_stl(path):
    data = Path(path).read_bytes()
    n = struct.unpack("<I", data[80:84])[0]
    if 84 + 50 * n == len(data):
        a = np.frombuffer(data[84:], dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]), count=n)
        return a["v"].astype(float)
    tris, cur = [], []  # ascii
    for line in data.decode().splitlines():
        if line.strip().startswith("vertex"):
            cur.append([float(x) for x in line.split()[1:4]])
            if len(cur) == 3:
                tris.append(cur); cur = []
    return np.array(tris)


def write_stl(path, tris):
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    n = np.divide(n, ln, out=np.zeros_like(n), where=ln > 0)
    with open(path, "wb") as f:
        f.write(b"Lisa Mouse (Logitech M185)".ljust(80, b"\0"))
        f.write(struct.pack("<I", len(tris)))
        for nn, t in zip(n, tris):
            f.write(struct.pack("<12fH", *nn, *t.flatten(), 0))


def render(path, tris):
    # Mesh is Z-up. Shade by face normal against a fixed light.
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    light = np.array([-0.4, -0.6, 0.8]); light /= np.linalg.norm(light)
    shade = 0.35 + 0.65 * np.abs(n @ light)
    colors = np.outer(shade, [0.84, 0.71, 0.64])
    fig = plt.figure(figsize=(4, 4), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(tris, facecolors=colors, linewidths=0))
    c = (tris.reshape(-1, 3).max(0) + tris.reshape(-1, 3).min(0)) / 2
    r = (tris.reshape(-1, 3).max(0) - tris.reshape(-1, 3).min(0)).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=30, azim=-55); ax.set_axis_off()
    fig.savefig(path, transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def main():
    src = Path(sys.argv[1])
    root = Path(__file__).resolve().parent.parent
    (root / "models").mkdir(exist_ok=True)
    (root / "images").mkdir(exist_ok=True)
    for name, out in PARTS.items():
        p = src / name
        tris = load_obj(p) if p.suffix == ".obj" else load_stl(p)
        write_stl(root / "models" / f"{out}.stl", tris)
        render(root / "images" / f"{out}.png", tris)
        d = tris.reshape(-1, 3).max(0) - tris.reshape(-1, 3).min(0)
        print(f"{out:22s} {len(tris):7d} tris  {d[0]:.1f} x {d[1]:.1f} x {d[2]:.1f} mm")


if __name__ == "__main__":
    main()
