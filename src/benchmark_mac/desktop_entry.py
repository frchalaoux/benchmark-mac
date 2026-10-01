"""Point d’entrée sans console pour le lanceur graphique Windows."""

import ctypes


def main() -> None:
    try:
        from .desktop import launch

        launch()
    except Exception as error:  # noqa: BLE001 - aucun terminal n'est ouvert par pythonw
        ctypes.windll.user32.MessageBoxW(  # type: ignore[attr-defined]
            None,
            f"PerfComparator n’a pas pu ouvrir son interface :\n{error}",
            "PerfComparator",
            0x10,
        )


if __name__ == "__main__":
    main()
