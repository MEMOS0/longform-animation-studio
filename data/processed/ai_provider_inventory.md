# AI provider inventory

| provider | modality | credential state | validation |
|---|---|---|---|
| `cloudflare_workers_ai` | text_generation | missing | smoke_passed_2026-11-26 |
| `cloudflare_workers_ai` | text_to_image | missing | flux-1-schnell smoke passed through temporary worker binding; production QA not complete |
| `cloudflare_workers_ai` | text_to_speech | missing | aura-2-en smoke passed through temporary worker binding; production voice QA not complete |
| `cloudflare_workers_ai` | video_generation | missing | no video-generation model visible in catalog audit on 2026-11-26 |
| `elevenlabs_browser_session` | voice_generation | not_required_or_external_session | historically validated on user's PC, unavailable in this VM-only session |

Credential state only says whether shell environment variables exist; it never prints secret values.
See `knowledge/production/ai-provider-inventory.md` for audited smoke-test evidence and caveats.
