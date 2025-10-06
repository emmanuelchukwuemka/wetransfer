# TODO List for Removing os.environ.get from Email Config

- [x] Edit app.py to replace EMAIL_SENDER with hardcoded value
- [x] Edit app.py to replace EMAIL_PASSWORD with hardcoded value
- [x] Edit app.py to replace EMAIL_RECEIVER with hardcoded value
- [x] Edit app.py to remove import os if not needed (not needed, os is used for PORT)
- [x] Verify changes in app.py
- [x] Test app locally (syntax check passed, user can run python app.py to test server)
- [ ] Deploy and test form submission
