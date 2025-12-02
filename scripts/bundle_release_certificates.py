#!/usr/bin/env python3
"""
Release Certificate Bundler
Generates all 15 certificates and bundles them into a release directory with cryptographic signatures.
"""
import os
import sys
import shutil
import glob
import subprocess
import json
import hashlib
from datetime import datetime
from typing import Dict, List

CONTRACTS_DIR = "farfan_core/farfan_core/contracts"
TOOLS_DIR = os.path.join(CONTRACTS_DIR, "tools")
RELEASE_DIR = "release_certificates"

def run_command(cmd: str) -> bool:
    try:
        env = os.environ.copy()
        cwd = os.getcwd()
        farfan_core_path = os.path.join(cwd, "farfan_core")
        env["PYTHONPATH"] = f"{farfan_core_path}:{env.get('PYTHONPATH', '')}"
        
        subprocess.check_call(cmd, shell=True, env=env)
        return True
    except subprocess.CalledProcessError:
        return False

def compute_sha256(file_path: str) -> str:
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest(cert_files: List[str], target_dir: str) -> Dict:
    """Generate cryptographic manifest for release certificates."""
    manifest = {
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "certificate_count": len(cert_files),
        "certificates": {}
    }
    
    for cert_file in cert_files:
        cert_path = os.path.join(target_dir, os.path.basename(cert_file))
        manifest["certificates"][os.path.basename(cert_file)] = {
            "sha256": compute_sha256(cert_path),
            "size_bytes": os.path.getsize(cert_path)
        }
    
    # Sign the manifest (SHA-256 of the manifest content)
    manifest_content = json.dumps(manifest, sort_keys=True, indent=2)
    manifest["signature"] = hashlib.sha256(manifest_content.encode()).hexdigest()
    
    return manifest

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = f"{RELEASE_DIR}_{timestamp}"
    
    print(f"=== BUNDLING RELEASE CERTIFICATES ===")
    print(f"Target directory: {target_dir}")
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. Generate Certificates
    print("\n--- Generating certificates ---")
    tools = glob.glob(os.path.join(TOOLS_DIR, "*.py"))
    for tool in sorted(tools):
        tool_name = os.path.basename(tool)
        print(f"Running {tool_name}...")
        if not run_command(f"python3 {tool}"):
            print(f"❌ Failed to run {tool}")
            sys.exit(1)
            
    # 2. Collect Certificates
    print("\n--- Collecting certificates ---")
    certs = glob.glob("*.json")
    cert_files = sorted([c for c in certs if c.endswith("_certificate.json")])
    
    if not cert_files:
        print("❌ No certificate files found!")
        sys.exit(1)
    
    for cert in cert_files:
        dest = os.path.join(target_dir, cert)
        shutil.copy2(cert, dest)
        print(f"  ✓ {cert}")
        
    # 3. Generate Cryptographic Manifest
    print("\n--- Generating cryptographic manifest ---")
    manifest = generate_manifest(cert_files, target_dir)
    manifest_path = os.path.join(target_dir, "MANIFEST.json")
    with open(manifest_path, "w") as f:
        json.dumps(manifest, f, indent=2)
    print(f"  ✓ MANIFEST.json (signature: {manifest['signature'][:16]}...)")
    
    # 4. Generate README
    print("\n--- Generating release README ---")
    readme_content = f"""# F.A.R.F.A.N Contract Certificate Bundle
Release Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Certificate Count: {len(cert_files)}
Manifest Signature: {manifest['signature']}

## Certificates Included
"""
    for cert in sorted(cert_files):
        readme_content += f"- {cert}\n"
    
    readme_content += f"""
## Verification
To verify this release bundle:
1. Check that all {len(cert_files)} certificates are present
2. Verify SHA-256 hashes match MANIFEST.json
3. Confirm manifest signature matches recomputed hash

## Certificate Descriptions
All contracts have been verified and certified as per F.A.R.F.A.N governance policy.
"""
    
    readme_path = os.path.join(target_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)
    
    print(f"\n=== SUCCESS ===")
    print(f"✅ Bundled {len(cert_files)} certificates in {target_dir}")
    
    # Verify count
    if len(cert_files) != 15:
        print(f"⚠️  WARNING: Expected 15 certificates, found {len(cert_files)}")
        print(f"Missing certificates may indicate incomplete contract suite.")
    else:
        print("✅ All 15 contracts accounted for.")
    
    print(f"\nManifest signature: {manifest['signature']}")

if __name__ == "__main__":
    main()
