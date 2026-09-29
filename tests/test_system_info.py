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


class FakeIdleProcess:
    pid = 0

    def cpu_percent(self, _interval=None) -> float:
        raise AssertionError("Le pseudo-processus PID 0 doit être ignoré.")


def test_macos_identity_uses_non_unique_hardware_fields_only(monkeypatch) -> None:
    payload = (
        '{"SPHardwareDataType":[{"machine_name":"MacBook Pro",'
        '"machine_model":"MacBookPro15,1","serial_number":"PRIVATE"}]}'
    )
    monkeypatch.setattr(system_info.sys, "platform", "darwin")
    monkeypatch.setattr(system_info, "_command", lambda *_args, **_kwargs: payload)

    identity = system_info._machine_identity()

    assert identity.manufacturer == "Apple"
    assert identity.product_name == "MacBook Pro"
    assert identity.model_identifier == "MacBookPro15,1"
    assert "PRIVATE" not in repr(identity)


def test_windows_identity_uses_cim_manufacturer_and_model(monkeypatch) -> None:
    payload = '{"Manufacturer":"ASUSTeK COMPUTER INC.","Model":"M1702QA"}'
    monkeypatch.setattr(system_info.sys, "platform", "win32")
    monkeypatch.setattr(system_info, "_command", lambda *_args, **_kwargs: payload)

    identity = system_info._machine_identity()

    assert identity.manufacturer == "ASUSTeK COMPUTER INC."
    assert identity.product_name == "M1702QA"
    assert identity.model_identifier == "M1702QA"


def test_linux_identity_uses_dmi_without_unique_identifiers(monkeypatch) -> None:
    values = {
        "/sys/devices/virtual/dmi/id/sys_vendor": "ASUSTeK COMPUTER INC.",
        "/sys/devices/virtual/dmi/id/product_name": "Vivobook M1702QA",
    }
    monkeypatch.setattr(system_info.sys, "platform", "linux")
    monkeypatch.setattr(system_info, "_hardware_text", values.get)

    identity = system_info._machine_identity()

    assert identity.manufacturer == "ASUSTeK COMPUTER INC."
    assert identity.product_name == "Vivobook M1702QA"
    assert identity.model_identifier == "Vivobook M1702QA"


def test_machine_readiness_warns_about_non_idle_state(monkeypatch) -> None:
    cpu_values = iter([0.0, 30.0])
    monkeypatch.setattr(
        system_info.psutil,
        "process_iter",
        lambda _attrs: [FakeIdleProcess(), FakeProcess()],
    )
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
