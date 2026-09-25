from types import SimpleNamespace

from benchmark_mac import system_info


class FakeProcess:
    pid = 42

    def __init__(self) -> None:
        self.calls = 0

    def cpu_percent(self, _interval=None) -> float:
        self.calls += 1
        return 0 if self.calls == 1 else 25

    def memory_percent(self) -> float:
        return 4

    def name(self) -> str:
        return "rendu-video"


def test_machine_readiness_warns_about_non_idle_state(monkeypatch) -> None:
    cpu_values = iter([0.0, 30.0])
    monkeypatch.setattr(system_info.psutil, "process_iter", lambda _attrs: [FakeProcess()])
    monkeypatch.setattr(system_info.psutil, "cpu_percent", lambda _interval=None: next(cpu_values))
    monkeypatch.setattr(
        system_info.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(total=100, available=10),
    )
    monkeypatch.setattr(system_info.psutil, "swap_memory", lambda: SimpleNamespace(percent=20))
    monkeypatch.setattr(system_info.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(system_info.os, "getpid", lambda: 999)

    snapshot = system_info.machine_readiness()

    assert not snapshot.suitable
    assert snapshot.cpu_percent == 30
    assert snapshot.memory_available_percent == 10
    assert snapshot.active_processes[0].name == "rendu-video"
    assert any("Charge CPU" in warning for warning in snapshot.warnings)
    assert any("Mémoire disponible" in warning for warning in snapshot.warnings)
    assert any("Processus actifs" in warning for warning in snapshot.warnings)
