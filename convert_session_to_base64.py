"""
Convert Telegram session file to Base64 format for GitHub Secrets
"""
import base64
import os

def convert_session_to_base64(session_file='nigeria_rain_monitor.session', output_file='session_base64.txt'):
    """
    Convert session file to base64 string
    """
    if not os.path.exists(session_file):
        print(f"❌ Error: {session_file} not found!")
        print("Please run 'python generate_session.py' first to create the session file.")
        return
    
    try:
        # Read session file
        with open(session_file, 'rb') as f:
            session_bytes = f.read()
        
        # Convert to base64
        session_base64 = base64.b64encode(session_bytes).decode('utf-8')
        
        # Save to file
        with open(output_file, 'w') as f:
            f.write(session_base64)
        
        print(f"✅ Session file converted successfully!")
        print(f"📄 Base64 string saved to: {output_file}")
        print(f"\n{'='*60}")
        print(f"Copy the content below and add it to GitHub Secrets:")
        print(f"Secret name: SESSION_STRING")
        print(f"{'='*60}\n")
        print(session_base64)
        print(f"\n{'='*60}")
        print(f"\n📋 Next steps:")
        print(f"1. Copy the base64 string above")
        print(f"2. Go to your GitHub repository")
        print(f"3. Settings → Secrets and variables → Actions")
        print(f"4. Click 'New repository secret'")
        print(f"5. Name: SESSION_STRING")
        print(f"6. Paste the base64 string")
        print(f"7. Click 'Add secret'")
        
    except Exception as e:
        print(f"❌ Error converting session: {e}")

if __name__ == "__main__":
    print("🔄 Converting session file to Base64...\n")
    convert_session_to_base64()
