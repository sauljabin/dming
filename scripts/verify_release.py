import argparse
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path


def one_artifact(dist: Path, pattern: str) -> Path:
    artifacts = list(dist.glob(pattern))
    if len(artifacts) != 1:
        raise ValueError(f"expected one {pattern} artifact, found {len(artifacts)}")
    return artifacts[0]


def verify_wheel(wheel: Path, version: str) -> None:
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
        metadata = BytesParser().parsebytes(archive.read(metadata_name))

        if metadata["Version"] != version:
            raise ValueError(f"wheel version is {metadata['Version']}, expected {version}")
        if metadata["License-Expression"] != "MIT AND CC-BY-4.0":
            raise ValueError("wheel does not declare the combined license expression")
        if not any(name.endswith(".dist-info/entry_points.txt") for name in names):
            raise ValueError("wheel does not contain console entry points")
        required_licenses = ("LICENSE", "NOTICE.md", "LICENSES/CC-BY-4.0.txt")
        for required in required_licenses:
            if not any(name.endswith(required) for name in names):
                raise ValueError(f"wheel does not contain {required}")


def verify_sdist(sdist: Path, version: str) -> None:
    expected_root = f"dming-{version}/"
    required = {
        "LICENSE",
        "LICENSES/CC-BY-4.0.txt",
        "NOTICE.md",
        "pyproject.toml",
        "dming/__init__.py",
        "dming/srd_data.py",
    }
    with tarfile.open(sdist, "r:gz") as archive:
        names = set(archive.getnames())

    missing = {path for path in required if f"{expected_root}{path}" not in names}
    if missing:
        raise ValueError(f"source distribution is missing: {', '.join(sorted(missing))}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify release distribution metadata.")
    parser.add_argument("version")
    parser.add_argument("dist", type=Path)
    args = parser.parse_args()

    wheel = one_artifact(args.dist, f"dming-{args.version}-*.whl")
    sdist = one_artifact(args.dist, f"dming-{args.version}.tar.gz")
    verify_wheel(wheel, args.version)
    verify_sdist(sdist, args.version)


if __name__ == "__main__":
    main()
