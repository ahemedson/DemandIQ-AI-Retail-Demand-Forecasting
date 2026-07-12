from pathlib import Path
import tempfile
import shutil


class ChartExporter:
    """
    Exports Plotly figures as high-resolution PNG images
    for inclusion in the Executive Intelligence Report.
    """

    def __init__(self):

        self.output_dir = Path(
            tempfile.mkdtemp(prefix="demandiq_report_")
        )

    # --------------------------------------------------
    # Export Single Figure
    # --------------------------------------------------

    def export(
        self,
        figure,
        filename,
        width=1400,
        height=700,
        scale=2
    ):

        path = self.output_dir / f"{filename}.png"

        figure.write_image(
            str(path),
            width=width,
            height=height,
            scale=scale
        )

        return str(path)

    # --------------------------------------------------
    # Export Multiple Figures
    # --------------------------------------------------

    def export_all(self, figures):

        exported = {}

        for name, figure in figures.items():

            exported[name] = self.export(
                figure,
                name
            )

        return exported

    # --------------------------------------------------
    # Cleanup Temporary Files
    # --------------------------------------------------

    def cleanup(self):

        if self.output_dir.exists():

            shutil.rmtree(
                self.output_dir,
                ignore_errors=True
            )