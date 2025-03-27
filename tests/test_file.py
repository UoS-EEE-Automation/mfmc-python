import pathlib

import mfmc


if __name__ == "__main__":
    f = mfmc.read.FileReader(pathlib.Path(__file__).parent /
                      "StainlessTest_500-4500_45dB.mfmc")

    probe = f.probes["PROBE<1>"]
    sequence = f.sequences["SEQUENCE<1>"]
    law = sequence.laws["LAW<1>"]

    for k, v in law.items():
        print(f"{k.lower()}: {v}")

    a = sequence.get_ascan(0)
    print(a)
