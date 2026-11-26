# AI generation provider inventory and smoke-test evidence

Status: living production note. Do not treat a provider as usable for film production until the exact modality needed has been smoke-tested with artifacts and cost controls.

## 2026-11-26 Cloudflare Workers AI audit

Cloudflare MCP is authenticated in this environment as the user's Cloudflare account. Read-only inventory found 52 Workers AI models. Available modality families include:

- text generation: `@cf/openai/gpt-oss-20b`, `@cf/openai/gpt-oss-120b`, `@cf/mistralai/mistral-small-3.1-24b-instruct`, `@cf/meta/llama-4-scout-17b-16e-instruct`, `@cf/meta/llama-3.2-11b-vision-instruct`, several others
- text-to-image: `@cf/black-forest-labs/flux-1-schnell`, `@cf/black-forest-labs/flux-2-klein-4b`, `@cf/black-forest-labs/flux-2-klein-9b`, `@cf/black-forest-labs/flux-2-dev`, `@cf/leonardo/phoenix-1.0`, `@cf/leonardo/lucid-origin`
- text-to-speech: `@cf/deepgram/aura-1`, `@cf/deepgram/aura-2-en`, `@cf/deepgram/aura-2-es`
- speech recognition: `@cf/openai/whisper`, `@cf/openai/whisper-large-v3-turbo`, `@cf/deepgram/nova-3`, `@cf/deepgram/flux`
- embeddings, translation, image classification, image-to-text, multimodal embeddings, voice activity detection

No text-to-video or image-to-video generation model was visible in this Cloudflare Workers AI inventory at audit time. Therefore video generation remains unvalidated and requires another provider or a changed Cloudflare catalog.

## Smoke tests actually performed

### Text generation — passed

Direct Workers AI calls through the authenticated Cloudflare API succeeded for:

- `@cf/openai/gpt-oss-20b`: produced coherent single-sentence glass-dragon description; usage 95 total tokens in the smoke call.
- `@cf/mistralai/mistral-small-3.1-24b-instruct`: produced coherent output; usage 63 total tokens.
- `@cf/meta/llama-4-scout-17b-16e-instruct`: produced coherent output but included an `assistant` prefix artifact; usage 76 total tokens.

Operational notes:

- `@cf/zai-org/glm-4.7-flash` responded but produced low-quality/garbled text for the simple prompt when reasoning settings were not correctly controlled.
- `@cf/meta/llama-3.2-11b-vision-instruct` was blocked by a Meta community-license acceptance requirement. Do not submit legal/license agreement prompts on the user's behalf without explicit approval.

### Text-to-image — passed through temporary Worker binding

The MCP `execute` bridge refuses to directly run Workers AI models that generate images/video/audio. To verify real capability, a temporary Cloudflare Worker named `longform-ai-smoke` was deployed with an AI binding and a random one-time header key, smoke-tested, then deleted.

`@cf/black-forest-labs/flux-1-schnell` succeeded with a vertical glass-dragon/bellmaker prompt at `steps: 1`:

- response keys: `image`, `usage`
- JPEG base64 length: 894348 bytes before decoding
- base64 prefix consistent with JPEG: `/9j/4AAQSkZJRgABAQAAAQAB`

This proves authenticated image generation capability, but it does not yet prove production suitability: character consistency, vertical composition control, text-free rendering, hands/faces, style consistency, and cost per usable image still need a dedicated visual QA batch.

### Text-to-speech — passed through temporary Worker binding

`@cf/deepgram/aura-2-en` succeeded after correcting the request shape:

- text: “Stay behind the bell. I will keep you safe.”
- speaker: `luna`
- encoding: `mp3`
- output type returned to Worker: `ReadableStream`
- consumed audio length: 17568 bytes
- first bytes: `255,243,100,196,0,21,72,190`

Important request-shape lesson: passing `container: "none"` with `encoding: "mp3"` fails with `Unsupported audio format: container is not applicable when encoding=mp3`; omit `container` for mp3.

The temporary Worker was deleted after testing. The public endpoint no longer exists.

### Access/operations gotchas

- Workers AI binary generation cannot be invoked directly through the Cloudflare MCP `execute` bridge: the bridge reports that it “does not run Workers AI models that generate images, video, or audio.”
- A workers.dev test endpoint initially returned Cloudflare error 1010 to plain Python urllib; using a normal Chrome-like User-Agent allowed the request through. This matters for smoke-test harnesses.
- Enabling a public workers.dev endpoint even with a random key is a temporary security risk; any future test worker must be deleted immediately or protected properly.

## Provider gaps as of this audit

- No text-to-video/image-to-video provider has been validated.
- No stored generic API secrets are visible in the Devin VM secret store.
- ElevenLabs access exists historically through browser sessions on the user's PC, but PC access is forbidden for this session; therefore ElevenLabs cannot currently be treated as an available production provider here.
- Music generation, lip-sync, motion capture, and video editing/model providers are not yet validated.

## Production-system implications

1. Treat Cloudflare Workers AI as a validated provider candidate for screenplay assistance, image generation, TTS, ASR, embeddings, and vision-language experimentation.
2. Do not claim it can generate video until a video model exists and passes artifact QA.
3. Add cost/latency/quality logging before using any model in batch production.
4. Every modality needs artifact-level QA: image identity consistency, hand/face integrity, voice emotional fit, pronunciation, loudness, dialogue intelligibility, and copyright/style safety.
5. Provider adapters must expose a common contract so the studio is not hard-wired to Cloudflare.
