# Add Helm and k3d to PATH
export PATH="$HOME/bin:$PATH"

# Verify installations
echo "=== Helm Version ==="
helm version
echo ""
echo "=== k3d Version ==="
k3d version
echo ""
echo "=== kubectl Version ==="
kubectl version --client
