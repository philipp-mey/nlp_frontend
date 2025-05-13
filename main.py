import subprocess


def run_streamlit_app():
    subprocess.run(["streamlit", "run", "src/frontend/app.py"])


if __name__ == "__main__":
    run_streamlit_app()
