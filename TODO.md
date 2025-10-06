# TODO List for Fixing Email Config for Deployment

- [x] Edit app.py to use os.environ.get for EMAIL_SENDER with fallback default
- [x] Edit app.py to use os.environ.get for EMAIL_PASSWORD with fallback default (use correct password from render.yaml)
- [x] Edit app.py to use os.environ.get for EMAIL_RECEIVER with fallback default
- [x] Verify changes in app.py
- [ ] Test app locally
- [ ] Deploy and test form submission
