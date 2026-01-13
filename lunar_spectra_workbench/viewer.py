import plotly.graph_objects as go
import numpy as np


def show_spectrum(
    analysis_result,
    shot_id,
    show_peaks=True,
    show_reference_lines=True
):
    combined = analysis_result.combined_spectra[shot_id]

    a = analysis_result.calibration["a"]
    b = analysis_result.calibration["b"]

    wavelength = a * combined["Pixel"].values + b
    intensity = combined["Combined_Normalized"].values

    fig = go.Figure()

    # --- main spectrum ---
    fig.add_trace(
        go.Scatter(
            x=wavelength,
            y=intensity,
            mode="lines",
            name="Combined spectrum",
            line=dict(width=2),
            hovertemplate="λ = %{x:.2f} nm<br>I = %{y:.3f}<extra></extra>"
        )
    )

    # --- detected peaks ---
    if show_peaks:
        matches = analysis_result.matches
        matches = matches[matches["shot_id"] == shot_id]

        peak_pixels = matches["Pixel"].values
        peak_wl = a * peak_pixels + b

        # Interpolate correct y-values from combined spectrum
        peak_int = np.interp(
            peak_wl,
            wavelength,
            intensity
        )

        peak_elements = matches["Element"].values
        peak_conf = matches["Confidence"].values
        peak_ref_wl = matches["Ref_wavelength_nm"].values

        fig.add_trace(
            go.Scatter(
                x=peak_wl,
                y=peak_int,
                mode="markers",
                name="Detected peaks",
                marker=dict(color="red", size=7),
                customdata=list(
                    zip(peak_elements, peak_ref_wl, peak_conf)
            ),
            hovertemplate=(
                "<b>Element:</b> %{customdata[0]}<br>"
                "<b>Detected λ:</b> %{x:.2f} nm<br>"
                "<b>Reference λ:</b> %{customdata[1]:.2f} nm<br>"
                "<b>Confidence:</b> %{customdata[2]:.2f}"
                "<extra></extra>"
            )
        )
    )


    # --- reference lines ---
    if show_reference_lines:
        try:
            from .reference_lines import REFERENCE_LINES

            for element, lines in REFERENCE_LINES.items():
                for wl in lines:
                    if wavelength.min() <= wl <= wavelength.max():
                        fig.add_vline(
                            x=wl,
                            line=dict(dash="dot", width=1),
                            opacity=0.3
                        )
        except ImportError:
            pass  # reference lines optional

    fig.update_layout(
        title=f"LIBS Spectrum Viewer — {shot_id}",
        xaxis_title="Wavelength (nm)",
        yaxis_title="Normalized intensity",
        hovermode="closest",
        template="plotly_white"
    )

    fig.show()
