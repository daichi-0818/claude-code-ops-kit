# claude-code-ops-kit

**AIコーディングエージェント（Claude Code等）を長時間・半自律で動かしたときに"サイレントに壊れる"問題への、実用キット。**

これは理念集でも原則リストでもありません。ここにある各パーツは、日々の実運用で実際に起きた障害から生まれたものです — 静かに発火しなくなった自動ジョブ、「データがゼロ」という報告が実は取得失敗だった件、修正の上に修正を積み重ねて誰もコードを理解できなくなった件。このキットは、それら一つ一つを今実際に防いでいる**運用の実物**です。そこが肝心で、エージェントを5分動かすのは簡単、腐らせずに数ヶ月動かすのが難しく、これはそこを支えるパーツ群です。

## 各コンポーネントが防ぐ失敗

| コンポーネント | 防ぐサイレント障害 |
|---|---|
| `skills/grilling` | 要件を詰めないまま作って作り違える（＋解決済みの作業を古いメモで再着手する） |
| `skills/systematic-debugging` | 当てずっぽう修正の積み重ね。延々と迷走する代わりに3回失敗で人間へエスカレーション |
| `skills/self-audit` | 裏取りのない数字や、取得失敗・古いチェックアウトが正体の「ゼロ／止まっている」主張を提出してしまう |
| `skills/pre-deploy` | import漏れや、本番ランタイムでしか出ないSyntaxErrorを積んだままデプロイしてしまう |
| `skills/tdd` | 構造上失敗できないテスト（トートロジー・実装密結合）と、失敗テスト無しの修正が再発する問題 |
| `skills/analysis-sweep` | 「全部読んで」が最初の派手な発見で静かに打ち切られる |
| `skills/cloud-run-job-deploy` | 中身空振りのexit 0や、スケジュールに追い越されて失敗が隠れるバッチJob |
| `agents/adversarial-verifier` | 書いた本人が自分の答案を採点する問題を、read-onlyの「壊れている前提」判定役で断つ |
| `agents/code-reviewer` | 人間のレビュアーが居ない場面で、二重チェック無しのまま出荷してしまう |
| `scripts/launchd-watchdog.py` | 定期自動処理が静かに死に、数週間誰も気づかない |
| `scripts/tidy.py` | 無限に伸びるノートと、実態から乖離した手管理INDEX |
| `templates/CLAUDE.global.md` | 新しいマシンのたびに運用ルールをゼロから再構築して、どれか1つを忘れる |

## コンポーネント

**Skills**（`skills/`）— 自動発動する規律:

1. **`grilling`** — 着手前の要件インタビュー。質問は1つずつ、各質問に自分の推奨回答を添え、入力／出力／人間の判断ポイント／除外事項が全部言語化できるまで。入口側のゲート。
2. **`systematic-debugging`** — 根本原因が分かるまで修正禁止。エラーを最後まで読み、再現し、境界を計測し、最小の変更を1つずつ。**3回失敗したら止めて人間へ**。
3. **`self-audit`** — 提出前の機械的な推測チェック。数値・事実の対ソース表、「ゼロ／止まっている／無い」の二重確認、断定と推測の分離、反証自問3件。
4. **`pre-deploy`** — デプロイ/push前のゲート。言語別静的解析（**本番ランタイムのバージョンで**確認）、import/依存チェック、テスト、env/secret配線、最終diffレビュー。1つでも落ちたらデプロイ中止。
5. **`tdd`** — seam基準のred→green。書く前に「テストすべき公開境界」を合意し、実装密結合・トートロジー・水平スライスを禁止。
6. **`analysis-sweep`** — 「全部読む」系タスクの完走規律。着手前にDoD5項目以上、2パス強制、途中報告禁止、反証自問3件、未確認領域の申告。
7. **`cloud-run-job-deploy`** — バッチのサイレント障害を防ぐJob固有手順。ロールバック先の記録が最初、imageのみ更新、ログ中身の検証（exit 0≠仕事をした）、監視登録、timeoutとトリガー間隔の整合。

**Agents**（`agents/`）— 独立した判定役:

- **`adversarial-verifier`** — 成果物を**壊れている前提（ASSUME BROKEN）**で反証しにいくread-onlyサブエージェント。品質レビューとは別の、懐疑的な「No」。
- **`code-reviewer`** — シニアエンジニア視点の品質レビュー（セキュリティ／エッジケース／性能／一貫性／プラットフォーム制約）。指摘はCRITICAL/WARNING/INFO＋`file:line`、CRITICALはデプロイをブロック。

**Scripts**（`scripts/`）:

- **`launchd-watchdog.py`** — macOSのlaunchdジョブを毎朝走査（ロード済みか／最終exit 0か／常駐デーモン生存／スクリプト実在／Label一致／TCC安全なパスか）し、異常があれば通知するウォッチドッグ。read-only。
- **`tidy.py`** — idempotentな日次片付け。ノートの月次アーカイブ、INDEX.md再生成、日付付きログのローテーション。ワークスペースを腐らせない。

**Template**（`templates/`）:

- **`CLAUDE.global.md`** — 規律一式を配線した、起点のグローバルCLAUDE.md雛形。検証ファースト、完了の証拠物ルール、生成/判定分離、無人運転の上限、コンテキスト衛生、複数案件マシンのデータ境界。

これらを貫く考え方 — 生成役と判定役の分離／無人運転の前に上限を明文化／人間の停止点を必ず残す／理解の腐敗を監視 — は [`docs/loop-engineering.md`](docs/loop-engineering.md) に。

## 導入

各パーツは独立。必要なものだけ取ってください。

```sh
# skills + agents（user-level。project-levelなら .claude/ へ）
cp -R skills/* ~/.claude/skills/
cp agents/*.md ~/.claude/agents/

# グローバルCLAUDE.md雛形 — 新しいマシン用。既存があれば手でマージ
cp -n templates/CLAUDE.global.md ~/.claude/CLAUDE.md

# watchdog（macOS）
python3 scripts/launchd-watchdog.py --prefix com.example.

# tidy（OS問わず）— まず必ずdry-run
python3 scripts/tidy.py --notes ~/notes/DAILY.md --archive-dir ~/notes/archive \
    --index-dir ~/notes --log-dir ~/notes/logs --dry-run
```

launchdでのwatchdog定期実行を含む詳細手順は [`docs/install.md`](docs/install.md) に。

スクリプトは標準ライブラリのみのPython 3で、全パスを引数で受けます（ハードコードパスなし）。skillのfrontmatter `description` は英語（自動発動の判定材料）。`self-audit` の宛先別ルール表は、自分の宛先で埋める雛形です。

## なぜ存在するか

このキットは、ある運用者の実際のClaude Code環境から抽出し、完全に汎用化したものです。名前・パス・業務ロジックは剥がしてあり、機構はそのまま。コーディングエージェントの危険は劇的なクラッシュより、静かな方 — 止まったジョブ、誰も二度見しなかった数字、もう誰も読まないコード — にあると同じ実感を持つ実務家に向けて公開します。

## ライセンス

MIT — [LICENSE](LICENSE) 参照。
