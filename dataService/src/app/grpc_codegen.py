from pathlib import Path


def ensure_grpc_generated() -> None:
    root_dir = Path(__file__).resolve().parents[2]
    proto_file = root_dir / "proto" / "patient_data.proto"
    output_dir = root_dir / "src" / "generated"
    pb2_file = output_dir / "patient_data_pb2.py"
    pb2_grpc_file = output_dir / "patient_data_pb2_grpc.py"

    if pb2_file.exists() and pb2_grpc_file.exists():
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    from grpc_tools import protoc

    result = protoc.main(
        [
            "grpc_tools.protoc",
            f"-I{proto_file.parent}",
            f"--python_out={output_dir}",
            f"--grpc_python_out={output_dir}",
            str(proto_file),
        ]
    )

    if result != 0:
        raise RuntimeError("Failed to generate gRPC Python files from proto/patient_data.proto")
