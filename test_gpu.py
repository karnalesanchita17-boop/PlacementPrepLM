
import torch

print("=== PlacementPrepLM: GPU Test ===")
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    device = torch.device("cuda")

    # Create two matrices on the GPU
    a = torch.rand(1000, 1000, device=device)
    b = torch.rand(1000, 1000, device=device)

    # Multiply the matrices on the GPU
    result = torch.matmul(a, b)

    print("GPU:", torch.cuda.get_device_name(0))
    print("Calculation completed successfully!")
    print("Result shape:", result.shape)
    print("Sample result:", result[0, 0].item())
else:
    print("GPU not available. Please check the installation.")
