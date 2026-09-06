# project-book output template

Use this asset only as the output skeleton. Replace every instructional line with repository-specific, evidence-backed content.

```text
project-book/
├── .learning-manifest.json      # schema version, Git baseline, sources, validation
├── 01-project-overview.md       # repository and subsystem overview
├── 02-installation.md           # safe installation and configuration
├── 03-architecture.md           # static, runtime, and deployment architecture
├── 04-core-flow.md              # representative end-to-end flows
├── 05-core-concepts.md          # real abstractions and contracts
├── 06-source-code-guide.md      # goal-oriented source navigation
├── 07-extension-guide.md        # project-native extension guidance
├── 08-examples.md               # illustrative and validated runnable examples
├── 09-faq.md                    # evidence-backed questions and answers
└── 10-learning-checklist.md     # coverage, validation, and practice checklist
```

Every chapter must state its analysis baseline, use repository-relative `path:line` evidence, and distinguish `已运行`, `静态验证`, `静态推断`, and `未运行`.
