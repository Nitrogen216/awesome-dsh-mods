# Awesome DSH Mods

个人维护的 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) Agent Preset 集合。每个 mode 都是一个可独立复制到 `$DSH_HOME/.agent-presets` 的真实目录。

## Modes

| Mode | 用途 | 状态 |
|---|---|---|
| [`dsh-autoresearch`](modes/dsh-autoresearch/) | 证据约束的自主科研、实验晋升与论文交付流水线 | Active |

## 安装

```sh
git clone https://github.com/Nitrogen216/awesome-dsh-mods.git
cd awesome-dsh-mods
./scripts/install-mode.sh dsh-autoresearch
```

安装脚本会把 mode 复制到 `${DSH_HOME:-$HOME/.dsh}/.agent-presets/<mode>`。DeepSeek Harness 的 preset 扫描只接受真实目录，因此脚本不创建符号链接。

如果目标已经存在，脚本会拒绝覆盖。确认要用仓库版本替换时：

```sh
./scripts/install-mode.sh --replace dsh-autoresearch
```

替换前，脚本会把原目录移动到带时间戳的同级备份。安装或更新后重启 DSH；仅修改 skill 或资源文件并不会让已有 preset generation 自动重载。

## 更新

```sh
git pull --ff-only
./scripts/install-mode.sh --replace dsh-autoresearch
```

DeepSeek Harness 的用户 preset 是完整配置快照，不会随官方 preset 自动升级。更新 Harness 后，应检查对应 mode 的 [`COMPATIBILITY.md`](modes/dsh-autoresearch/COMPATIBILITY.md) 并重新运行验证命令。

## 安全边界

本仓库只保存 mode 源文件。不要提交以下机器级数据：

- `$DSH_HOME/.credentials.yaml`
- `$DSH_HOME/settings.yaml`
- `$DSH_HOME/sessions/`
- `$DSH_HOME/storages/`
- `.env`、API keys、tokens 或浏览器登录状态

第三方来源与许可证记录在各 mode 的 `THIRD_PARTY_NOTICES.md` 中。
