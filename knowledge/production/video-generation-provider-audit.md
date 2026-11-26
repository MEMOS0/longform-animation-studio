# External video-generation provider audit

Updated: 2026-11-26. This is documentation research, not a paid smoke test. No provider terms were accepted, no keys were created, and no generation spending occurred. Exact availability/pricing must be rechecked immediately before production because this market changes quickly.

## Key correction to earlier inventory

Cloudflare Workers AI still shows no video-generation model in our audited catalog, but external video APIs do exist. The earlier gap was provider-specific, not a market-wide absence.

## Most useful current inventory

| provider/API | current documented video models | documented capability | documented cost signal | production note |
|---|---|---|---|---|
| Runway Dev | `gen4.5`, `gen4_turbo`, `aleph2` plus routed third-party models | Runway text/image-to-video, editing; API also exposes Google/Kling/ByteDance/MiniMax/Alibaba/xAI models | `gen4_turbo` $0.05/sec; `gen4.5` $0.12/sec; `aleph2` $0.28/sec | strongest single-vendor aggregation point; pay-as-you-go credits; outputs claimed as owned by customer on pricing page |
| Runway Dev routed Google | `gemini_omni_flash_1.2` | text/keyframes/references to video, editing and extension; 360p–4K | from $0.02/sec | potentially cost-efficient draft/iteration lane; exact quality/consistency untested |
| Runway Dev routed Kling | `kling_4_flash`, `kling_4`, `kling3.0_pro`, `klingO3_pro` | text/frame/reference video, editing, optional/native audio depending on model | `kling_4_flash` from $0.094/sec; `kling_4` from $0.157/sec | 3–30s clip lengths make it a shot-generation tool, not a whole-film tool |
| Runway Dev routed ByteDance | `seedance2_5`, `seedance2_5_flash`, `seedance2`, `seedance2_fast`, `seedance2_mini` | cinematic video up to 30s with image/video/audio references | `seedance2_mini` from $0.07/sec; `seedance2_5` from $0.20/sec | potentially strong cinematic/reference-control lane; validate character consistency |
| Runway Dev routed Alibaba | `wan3`, `wan3_prime` | native audio, 2–30s, image/video/audio references, up to 1080p | `wan3` from $0.05/sec | cost-efficient candidate for dialogue/performance shots if consistency holds |
| Runway Dev routed xAI | `grok_imagine_1_5`, `grok_imagine_1_5_lite` | fast video with native audio/reference images; Lite from text/start frame | Lite from $0.02/sec | potentially cheap draft lane; needs quality/safety/licensing review |
| Google Gemini API direct | `gemini-omni-1.2-flash`, `genie-4` | Omni Flash: 3–15s videos with native audio and conversational editing. Genie 4: real-time interactive world generation | pricing not verified in this audit | Veo 3.1 Preview in Gemini API shut down 2026-10-22; do not build new plans around it |
| Luma Agents API | `ray-3.2` | text-to-video, image-to-video, video edit/reframe/extend; 360p–1080p documented | billed per 5-second block; exact dollar credit rate plan-dependent | useful independent fallback; no smoke test yet |
| Pika API | `pika-2.5` plus catalog operations | async text-to-video endpoint; 5/10s, up to 1080p, multiple aspect ratios including 9:16 | billing metadata returned per job; exact price not audited | public catalog is useful because it can be inspected without a key |
| Kling direct API | Kling 4.0 / 4.0 Flash | direct Singapore API; resource packages; 4K/HDR options for 4.0 | 4.0 no-input documented at $0.157/sec 720p, $0.235/sec 1080p, $0.549/sec 4K | direct API adds procurement/resource-pack complexity compared with Runway aggregation |
| OpenAI Videos API | `sora-2`, `sora-2-pro` | historical only | unavailable | shut down 2026-09-24; no one-to-one replacement according to current docs |

## Cost reality for long-form production

Per-second prices look small until converted to finished minutes:

- `$0.02/sec` → `$1.20` per finished minute, before iteration.
- `$0.05/sec` → `$3.00` per finished minute.
- `$0.12/sec` → `$7.20` per finished minute.
- `$0.157/sec` → `$9.42` per finished minute.
- `$0.28/sec` → `$16.80` per finished minute.

A 48-minute film therefore costs roughly **$58–$806 in raw generation** if every finished second were generated exactly once at those rates. Real production requires iteration, alternates, failed shots, pickup shots, and continuity corrections. A conservative 5–15x generation-to-final ratio implies roughly **$288–$12,096** depending on model mix and discipline. This does not include voice, music, edit, sound design, review, or human/agent labor.

Production implication: long-form cannot be treated as “generate 48 minutes.” It must be engineered as a shot pipeline:

1. create strong keyframes/character sheets cheaply;
2. generate only motion-critical shots with expensive video models;
3. reuse backgrounds/turnarounds/expressions where legally and aesthetically valid;
4. use cheaper draft models for blocking and expensive models only for final hero shots;
5. track generation-to-final ratio as a production KPI;
6. validate character consistency before choosing the cheapest model.

## Pre-spend validation protocol

Before any paid generation:

1. Read the exact current operation schema, not just marketing docs.
2. Confirm output ownership/license, data retention, content restrictions, watermarking, and commercial-use terms.
3. Confirm price at target resolution/duration/aspect ratio and whether input video/reference duration is billed.
4. Run a fixed smoke pack: same character closeup, creature child shot, two-character dialogue, transformation shot, and continuity sequence.
5. Store cost, latency, failures, seed/reference controls, output resolution, artifacts, and license URL in repo evidence.
6. Do not accept terms, create billing, or spend money without explicit user approval.

## Source URLs inspected

- https://docs.dev.runwayml.com/guides/models/
- https://dev.runway.com/pricing
- https://aistudio.google.com/docs/video
- https://ai.google.dev/gemini-api/docs/video
- https://docs.agents.lumalabs.ai/api/resources/generations/methods/create/
- https://docs.agents.lumalabs.ai/guides/pricing/
- https://kling.ai/document-api/pricing/base/video.md
- https://dev.pika.art/models/quick-start
- https://dev.pika.art/llms/pika/pika-2.5/text-to-video
- https://developers.openai.com/api/docs/guides/video-generation
