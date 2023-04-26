import definitions
import mfmc


if __name__ == "__main__":
    f = mfmc.File(
        definitions.PROJECT_ROOT / "tests" / "StainlessTest_500-4500_45dB.mfmc"
    )

    probe = f.probes["PROBE<1>"]
    sequence = f.sequences["SEQUENCE<1>"]
    law = sequence.laws["LAW<1>"]

    for k, v in law.items():
        print(f"{k.lower()}: {v}")
