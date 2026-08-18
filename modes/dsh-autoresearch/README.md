# dsh-autoresearch

`dsh-autoresearch` 是基于 DeepSeek Harness `code` preset 扩展的科研 mode。它把已有项目改进、宽泛方向收敛、实验筛选、全量确认、证据晋升和论文交付组织为一个可恢复的 V4 流水线。

## 主要组成

- `agent.cordis.yml`：Agent Plane 组合、persona、工具与运行时策略
- `skills/`：21 个 mode 私有技能；默认 skill roots 被隔离
- `plugins/skill-isolation.mjs`：限制自动 skill 加载范围
- `plugins/oracle-governor.mjs`：限制 Oracle 只能按经过授权的浏览器 Pro 路径运行
- `tools/transition_guard.py`：持久化并校验科研阶段转换
- `templates/` 与 `references/`：研究和论文交付模板
- `vendor/aris-upstream/`：固定的 ARIS 上游文件快照

## 安装

从仓库根目录运行：

```sh
./scripts/install-mode.sh dsh-autoresearch
```

随后在 DSH 的 Agent Preset 选择器中选择 `dsh-autoresearch`。机器级凭据、模型选择和浏览器登录状态不随 mode 分发，需要在新机器单独配置。

## 可选本机依赖

- Oracle 路径要求可执行的 `oracle` CLI，并在浏览器中具备所请求的 ChatGPT Pro 能力。
- `subagent_codex` 与 `subagent_claude_code` 要求活动 Profile 在 Host Plane 安装并挂载对应 provider；缺少 provider 时，科研主流程仍可运行，但相关外部审查不可用。
- 长训练任务依赖目标项目自己的 Python/GPU/SSH 环境，本 mode 不携带这些环境。

## 验证

在仓库根目录执行静态与状态机测试：

```sh
python3 -B -m unittest discover -s modes/dsh-autoresearch/tools/tests -p 'test_*.py'
```

运行插件测试时，把 `<deepseek-harness>` 换成已经构建的 Harness 源码目录：

```sh
cd <deepseek-harness>
node --test /absolute/path/to/awesome-dsh-mods/modes/dsh-autoresearch/tools/tests/test_runtime_plugins.mjs
```

升级 Harness 后还应启动一个新的 `dsh-autoresearch` 会话，检查 preset mount、skill catalog、Code Mode、后台任务和可选 reviewer provider。
