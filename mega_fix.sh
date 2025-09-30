# --- MEGA FIX SCRIPT FOR PNPM INSTALLATION ISSUES ---
# This script attempts to resolve persistent pnpm installation and dependency issues.
# It will try to:
# 1. Clean up conflicting pnpm/pnpx executables from Homebrew's path.
# 2. Update/install pnpm globally via npm.
# 3. Enable pnpm via corepack.
# 4. Clean up project-level node_modules and pnpm-lock.yaml.
# 5. Reinstall project dependencies.
# 6. Verify pnpm version and next-pwa installation.

# --- WARNING ---
# This script uses 'sudo' to remove files in system directories.
# You will be prompted for your password. Please review the script before running.
# --- WARNING ---

echo "--- Starting MEGA PNPM Fix Script ---"

# --- Step 1: Clean up conflicting executables ---
echo "1. Cleaning up conflicting pnpm/pnpx executables from /opt/homebrew/bin..."
# Check if pnpm exists and remove it
if [ -f "/opt/homebrew/bin/pnpm" ]; then
    echo "  - Found /opt/homebrew/bin/pnpm. Removing..."
    sudo rm /opt/homebrew/bin/pnpm || { echo "Error: Failed to remove /opt/homebrew/bin/pnpm. Aborting."; exit 1; }
else
    echo "  - /opt/homebrew/bin/pnpm not found. Skipping."
fi

# Check if pnpx exists and remove it
if [ -f "/opt/homebrew/bin/pnpx" ]; then
    echo "  - Found /opt/homebrew/bin/pnpx. Removing..."
    sudo rm /opt/homebrew/bin/pnpx || { echo "Error: Failed to remove /opt/homebrew/bin/pnpx. Aborting."; exit 1; }
else
    echo "  - /opt/homebrew/bin/pnpx not found. Skipping."
fi

echo "Cleanup of conflicting executables complete."

# --- Step 2: Install/Update pnpm globally via npm ---
echo "2. Attempting to install/update pnpm globally via npm..."
npm install -g pnpm@latest || { echo "Error: npm global install of pnpm failed. Aborting."; exit 1; }
echo "npm global install of pnpm attempted."

# --- Step 3: Enable pnpm via corepack ---
echo "3. Enabling pnpm via corepack..."
# Check if corepack is available (Node.js >= 16.9)
if command -v corepack &> /dev/null; then
    corepack enable pnpm || { echo "Error: corepack enable pnpm failed. Aborting."; exit 1; }
    echo "corepack enabled for pnpm."
else
    echo "  - corepack not found or Node.js version is too old. Skipping corepack enablement."
fi

# --- Step 4: Verify pnpm version ---
echo "4. Verifying pnpm version..."
pnpm_version=$(pnpm -v)
echo "  - Current pnpm version: $pnpm_version"
if [[ "$pnpm_version" == "10.17.1" ]]; then
    echo "Warning: pnpm is still at version 10.17.1. This may cause further issues."
    echo "Please consider investigating your Node.js/npm/Homebrew environment further."
else
    echo "  - pnpm updated successfully to a newer version."
fi

# --- Step 5: Clean up project-level dependencies ---
echo "5. Cleaning up project-level node_modules and pnpm-lock.yaml..."
# Navigate to project root (assuming script is run from root or sub-directory)
# This script assumes it's run from the project root or a sub-directory where 'MEGA' is the root.
# Let's ensure we are in the MEGA root.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="/Volumes/macmini/projs/ECGiga/MEGA" # Explicitly set project root

# If the script is run from a sub-directory, we need to cd to the root
if [[ "$SCRIPT_DIR" != "$PROJECT_ROOT" ]]; then
    echo "  - Changing directory to project root: $PROJECT_ROOT"
    cd "$PROJECT_ROOT" || { echo "Error: Failed to change to project root. Aborting."; exit 1; }
fi

if [ -d "node_modules" ]; then
    echo "  - Removing existing node_modules directory..."
    rm -rf node_modules || { echo "Error: Failed to remove node_modules. Aborting."; exit 1; }
else
    echo "  - node_modules directory not found. Skipping."
fi

if [ -f "pnpm-lock.yaml" ]; then
    echo "  - Removendo existing pnpm-lock.yaml..."
    rm pnpm-lock.yaml || { echo "Error: Failed to remove pnpm-lock.yaml. Aborting."; exit 1; }
else
    echo "  - pnpm-lock.yaml not found. Skipping."
fi
echo "Project-level cleanup complete."

# --- Step 6: Reinstall project dependencies ---
echo "6. Reinstalling project dependencies with the (hopefully) updated pnpm..."
pnpm install || { echo "Error: pnpm install failed. Please check the output above."; exit 1; }
echo "Project dependencies reinstalled."

# --- Step 7: Verify next-pwa installation ---
echo "7. Verifying next-pwa installation in apps/web..."
cd apps/web || { echo "Error: Failed to change to apps/web directory. Aborting."; exit 1; }

# Verify package.json
if grep -q "next-pwa" package.json; then
    echo "  - 'next-pwa' found in apps/web/package.json."
else
    echo "Error: 'next-pwa' NOT found in apps/web/package.json. This is unexpected."
fi

# Verify pnpm-lock.yaml (from root)
cd "$PROJECT_ROOT" # Go back to root to check lockfile
if grep -q "next-pwa" pnpm-lock.yaml; then
    echo "  - 'next-pwa' found in pnpm-lock.yaml."
else
    echo "Error: 'next-pwa' NOT found in pnpm-lock.yaml. Lockfile is still inconsistent."
fi

# Verify physical presence in node_modules
if [ -d "node_modules/next-pwa" ]; then
    echo "  - 'next-pwa' physically present in node_modules."
else
    echo "Error: 'next-pwa' NOT physically present in node_modules. Installation failed."
fi

echo "--- MEGA PNPM Fix Script Finished ---"
echo "Please review the output above for any errors or warnings."
echo "If pnpm version is still 10.17.1, manual intervention for your system's pnpm installation is required."
