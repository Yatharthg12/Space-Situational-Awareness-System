import plotly.graph_objects as go
import numpy as np


def plot_orbits(trajectories, output_html="outputs/orbits.html"):
    fig = go.Figure()

    # Earth (simple sphere)
    R = 6371  # km
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j]
    x = R * np.cos(u) * np.sin(v)
    y = R * np.sin(u) * np.sin(v)
    z = R * np.cos(v)

    fig.add_surface(
        x=x, y=y, z=z,
        colorscale="Blues",
        opacity=0.6,
        showscale=False
    )

    # Plot orbits
    for obj in trajectories.values():
        xs = [p["x"] for p in obj["trajectory"]]
        ys = [p["y"] for p in obj["trajectory"]]
        zs = [p["z"] for p in obj["trajectory"]]

        if obj["type"] == "station":
            color = "red"
        elif obj["type"] == "satellite":
            color = "green"
        else:
            color = "orange"

        fig.add_trace(go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode="lines",
            line=dict(width=2, color=color),
            name=obj["name"]
        ))

    fig.update_layout(
        title="Space Situational Awareness: Orbital Overview",
        scene=dict(
            xaxis_title="X (km)",
            yaxis_title="Y (km)",
            zaxis_title="Z (km)",
            aspectmode="data"
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    fig.write_html(output_html)
