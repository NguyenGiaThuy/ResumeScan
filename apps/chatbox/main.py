"""
AI Elevate Interview System - Main Entry Point

This is the main entry point for the AI Elevate Interview System.
The application has been modularized for better maintainability and organization.
"""

from app import InterviewApp


def main():
    """Main application entry point"""
    app = InterviewApp()
    app.run()


if __name__ == "__main__":
    main()
