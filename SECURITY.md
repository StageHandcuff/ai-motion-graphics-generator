# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

Open a private security advisory on GitHub, or email
`security@ai-motion-graphics-generator.dev` with:

- affected version (`python -m bootstrap.cli --version`)
- a minimal reproduction (input file, preset, driver)
- the exact command you ran

We aim to triage within 72 hours.

## Threat model

This is a local desktop tool. It shells out to `ffmpeg` and optionally to
`afterfx.exe` / `blender.exe`. The realistic attack surface is:

1. **Malicious project files** — `.amgproj` and `.mogrt` inputs are parsed
   with `yaml.safe_load` and `json.loads` only. Never `eval`, never
   `pickle` on user-supplied paths.
2. **Model weight downloads** — remote weights are verified against a
   pinned SHA-256 in `config/models.lock.json`. If a hash mismatches, the
   download is aborted and the file is deleted.
3. **Subprocess invocation** — all `subprocess` calls go through
   `utils/subprocess_safe.run()` which forbids `shell=True` and validates
   argv against an allowlist of binaries.
4. **Plugin loading** — third-party drivers are loaded only from
   `%APPDATA%/ai-motion-graphics-generator/plugins/` and require a
   `plugin.toml` with a `sha256` field.

If you find a way to escape any of the above, that's a CVE and we want it.