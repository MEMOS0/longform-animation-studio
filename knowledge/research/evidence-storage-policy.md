# Evidence storage policy

Repository evidence must be durable, inspectable, and small enough for agent handoff. Commit derived evidence: contact sheets, timelines, second-resolution metrics, media summaries, subtitle files, thumbnails, manifests, and timestamped analyses. Do not commit full source videos except when the user explicitly asks for archival storage; large source media should remain in local/object storage or be re-downloaded from the source when rights and access permit.

Rationale: full videos make the repository slow and do not themselves prove they were watched. The inspectable research artifact is the timestamped derived evidence plus the written scene-level interpretation. Every analysis must state whether it used continuous viewing, sampled full-runtime contact sheets, subtitles, machine metrics, or metadata only.

Current action: the `no72LZAVvZQ` source video was removed after the initial commit because GitHub warned about large files; its contact sheets, timelines, metrics, summary, thumbnail, and written analysis remain in the repository.
