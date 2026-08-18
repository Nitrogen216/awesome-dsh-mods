#!/usr/bin/env node

import assert from 'node:assert/strict'
import { test } from 'node:test'
import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'

const root = process.cwd()
const { Context } = await import(pathToFileURL(resolve(root, 'vendor/cordis/lib/index.js')).href)
const { default: SystemPrompt } = await import(pathToFileURL(resolve(root, 'packages/core/system-prompt/lib/index.js')).href)
const { default: ToolRuntime } = await import(pathToFileURL(resolve(root, 'packages/core/tools/lib/index.js')).href)
const skillIsolation = await import(new URL('../../plugins/skill-isolation.mjs', import.meta.url))
const oracleGovernor = await import(new URL('../../plugins/oracle-governor.mjs', import.meta.url))

const signal = new AbortController().signal

function fakeAgent(userText = 'Please ask Oracle to resolve this decision.') {
  return {
    id: 'autoresearch-test-agent',
    session: {
      header: { cwd: root },
      events: [{
        type: 'user/message',
        data: {
          source: { kind: 'user' },
          content: [{ type: 'text', text: userText }],
        },
      }],
    },
  }
}

async function setup() {
  const ctx = new Context()
  await ctx.plugin(SystemPrompt)
  await ctx.plugin(ToolRuntime, { mode: 'native' })
  return ctx
}

function textOf(result) {
  return result.content.filter(block => block.type === 'text').map(block => block.text).join('\n')
}

let callNumber = 0
function execute(ctx, name, args, agent) {
  callNumber += 1
  return ctx.tools.execute({
    signal,
    callId: 'runtime-policy-' + callNumber,
    name,
    arguments: args,
    agent,
  })
}

function registerTextTool(ctx, name, handler) {
  ctx.tools.register({
    name,
    description: 'Runtime-policy test fixture.',
    parameters: { type: 'object', additionalProperties: true },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    execute: handler,
  })
}

function decisionPacket(overrides = {}) {
  return {
    basis: 'major_decision',
    decision_id: 'mapping:mechanism-family:v1',
    decision: 'Choose the central mechanism family for the next attributable adaptation.',
    material_consequence: 'central_mechanism_family',
    alternatives: ['adapt family A', 'adapt family B'],
    evidence: {
      baseline: 'The comparable baseline fails in the measured sparse regime.',
      literature: 'Both primary papers report controlled gains under matching assumptions.',
      experiments: 'The current screens do not distinguish the mechanisms.',
      unresolved: 'Their assumptions overlap on the observed regime.',
    },
    immediate_actions: ['implement the family A insertion', 'implement the family B replacement'],
    files: ['package.json'],
    ...overrides,
  }
}

test('skill isolation allows only the configured preset catalog', async () => {
  const ctx = await setup()
  registerTextTool(ctx, 'skill', args => Promise.resolve(args.name))
  await ctx.plugin(skillIsolation, { allowedSkills: ['paper-writing', 'literature-research'] })
  const agent = fakeAgent()

  const allowed = await execute(ctx, 'skill', { name: 'paper-writing' }, agent)
  assert.equal(allowed.isError, false)
  assert.equal(textOf(allowed), 'paper-writing')

  const denied = await execute(ctx, 'skill', { name: 'external-review-loop' }, agent)
  assert.equal(denied.isError, true)
  assert.match(textOf(denied), /curated preset skills/)

  await ctx.fiber.dispose()
})

test('Oracle shell execution is denied without a runtime authorization', async () => {
  const ctx = await setup()
  registerTextTool(ctx, 'bash', () => Promise.resolve('ok'))
  await ctx.plugin(oracleGovernor)
  const agent = fakeAgent()

  for (const command of [
    'oracle --engine browser -p test',
    'env oracle --engine browser -p test',
    'nohup oracle --engine browser -p test',
    'npx -y @steipete/oracle --engine browser -p test',
  ]) {
    const denied = await execute(ctx, 'bash', { command, description: 'bypass attempt' }, agent)
    assert.equal(denied.isError, true)
    assert.match(textOf(denied), /Oracle consultation denied/)
  }

  const status = await execute(ctx, 'bash', {
    command: 'oracle status --hours 72',
    description: 'inspect existing sessions',
  }, agent)
  assert.equal(status.isError, false)

  const ordinarySearch = await execute(ctx, 'bash', {
    command: "rg -n 'oracle' README.md",
    description: 'search ordinary text',
  }, agent)
  assert.equal(ordinarySearch.isError, false)

  await ctx.fiber.dispose()
})

test('Oracle authorization requires an exact successful dry-run before a background run', async () => {
  const ctx = await setup()
  registerTextTool(ctx, 'bash', args => Promise.resolve(
    args.run_in_background === true ? 'started background job bash-1' : 'dry run ok',
  ))
  await ctx.plugin(oracleGovernor, {
    executable: 'oracle',
    engine: 'browser',
    model: 'gpt-5.6-sol',
    thinkingTime: 'pro',
    maxFiles: 8,
  })
  const agent = fakeAgent()

  const approval = await execute(ctx, 'oracle_governor', decisionPacket(), agent)
  assert.equal(approval.isError, false)
  const authorization = approval.value
  assert.equal(authorization.verdict, 'consult_oracle')
  assert.match(authorization.dryRunCommand, /--dry-run summary --files-report/)
  assert.match(authorization.runCommand, /--browser-thinking-time 'pro'/)

  const premature = await execute(ctx, 'bash', {
    command: authorization.runCommand,
    description: 'premature Oracle run',
    run_in_background: true,
  }, agent)
  assert.equal(premature.isError, true)
  assert.match(textOf(premature), /only after its dry-run succeeds/)

  const altered = await execute(ctx, 'bash', {
    command: authorization.dryRunCommand + ' --verbose',
    description: 'altered dry run',
  }, agent)
  assert.equal(altered.isError, true)
  assert.match(textOf(altered), /exact command/)

  const relocated = await execute(ctx, 'bash', {
    command: authorization.dryRunCommand,
    description: 'relocated dry run',
    workdir: '/tmp',
  }, agent)
  assert.equal(relocated.isError, true)
  assert.match(textOf(relocated), /session workspace/)

  const dry = await execute(ctx, 'bash', {
    command: authorization.dryRunCommand,
    description: 'authorized dry run',
  }, agent)
  assert.equal(dry.isError, false)

  const foreground = await execute(ctx, 'bash', {
    command: authorization.runCommand,
    description: 'foreground Oracle run',
  }, agent)
  assert.equal(foreground.isError, true)
  assert.match(textOf(foreground), /must start through a background DSH job/)

  const run = await execute(ctx, 'bash', {
    command: authorization.runCommand,
    description: 'authorized Oracle run',
    run_in_background: true,
  }, agent)
  assert.equal(run.isError, false)
  assert.match(textOf(run), /started background job/)

  const repeated = await execute(ctx, 'oracle_governor', decisionPacket(), agent)
  assert.equal(repeated.isError, false)
  assert.equal(repeated.value.verdict, 'continue_local')

  await ctx.fiber.dispose()
})

test('explicit-user basis quotes the current human request and packet validation stays narrow', async () => {
  const ctx = await setup()
  await ctx.plugin(oracleGovernor)
  const agent = fakeAgent('请使用 Oracle 帮我决定这个重大选择。')

  const accepted = await execute(ctx, 'oracle_governor', decisionPacket({
    basis: 'explicit_user_request',
    decision_id: 'user:mechanism-choice:v1',
    user_request_excerpt: '请使用 Oracle 帮我决定这个重大选择。',
  }), agent)
  assert.equal(accepted.isError, false)

  const unsupported = await execute(ctx, 'oracle_governor', decisionPacket({
    decision_id: 'mapping:too-few-options:v1',
    alternatives: ['only one option'],
    immediate_actions: ['implement it'],
  }), agent)
  assert.equal(unsupported.isError, true)
  assert.match(textOf(unsupported), /alternatives must contain 2-3 entries/)

  await ctx.fiber.dispose()
})

test('Code Mode session replay restores the dry-run authorization state', async () => {
  const first = await setup()
  await first.plugin(oracleGovernor)
  const initialAgent = fakeAgent()
  const approval = await execute(first, 'oracle_governor', decisionPacket({
    decision_id: 'confirmation:protocol-choice:v1',
    material_consequence: 'protocol_contradiction_or_expensive_confirmation',
  }), initialAgent)
  assert.equal(approval.isError, false)
  const authorization = approval.value
  await first.fiber.dispose()

  const replayAgent = fakeAgent()
  replayAgent.id = 'autoresearch-replay-agent'
  replayAgent.session.events.push(
    {
      type: 'tool/code-dispatch',
      data: {
        name: 'oracle_governor',
        arguments: decisionPacket({ decision_id: 'confirmation:protocol-choice:v1' }),
        isError: false,
        content: [{ type: 'text', text: JSON.stringify(authorization) }],
      },
    },
    {
      type: 'tool/code-dispatch',
      data: {
        name: 'bash',
        arguments: { command: authorization.dryRunCommand, description: 'authorized dry run' },
        isError: false,
        content: [{ type: 'text', text: 'dry run ok' }],
      },
    },
  )

  const resumed = await setup()
  registerTextTool(resumed, 'bash', () => Promise.resolve('started background job bash-2'))
  await resumed.plugin(oracleGovernor)
  const run = await execute(resumed, 'bash', {
    command: authorization.runCommand,
    description: 'resume authorized Oracle run',
    run_in_background: true,
  }, replayAgent)
  assert.equal(run.isError, false)
  assert.match(textOf(run), /started background job/)

  await resumed.fiber.dispose()
})

test('an unsettled Code Mode Oracle start cannot be submitted twice after recovery', async () => {
  const first = await setup()
  await first.plugin(oracleGovernor)
  const initialAgent = fakeAgent()
  const approval = await execute(first, 'oracle_governor', decisionPacket({
    decision_id: 'promotion:claim-freeze:v1',
    material_consequence: 'promotion_freeze_or_reject',
  }), initialAgent)
  const authorization = approval.value
  await first.fiber.dispose()

  const replayAgent = fakeAgent()
  replayAgent.id = 'autoresearch-unsettled-agent'
  replayAgent.session.events.push(
    {
      type: 'tool/code-dispatch',
      data: {
        name: 'oracle_governor',
        arguments: decisionPacket({ decision_id: 'promotion:claim-freeze:v1' }),
        isError: false,
        content: [{ type: 'text', text: JSON.stringify(authorization) }],
      },
    },
    {
      type: 'tool/code-dispatch',
      data: {
        name: 'bash',
        arguments: { command: authorization.dryRunCommand, description: 'authorized dry run' },
        isError: false,
        content: [{ type: 'text', text: 'dry run ok' }],
      },
    },
    {
      type: 'tool/code-dispatch-start',
      data: {
        name: 'bash',
        arguments: {
          command: authorization.runCommand,
          description: 'started but not settled',
          run_in_background: true,
        },
      },
    },
  )

  const resumed = await setup()
  registerTextTool(resumed, 'bash', () => Promise.resolve('started background job bash-3'))
  await resumed.plugin(oracleGovernor)
  const duplicate = await execute(resumed, 'bash', {
    command: authorization.runCommand,
    description: 'duplicate Oracle run',
    run_in_background: true,
  }, replayAgent)
  assert.equal(duplicate.isError, true)
  assert.match(textOf(duplicate), /only after its dry-run succeeds/)

  const status = await execute(resumed, 'bash', {
    command: 'oracle status --hours 72',
    description: 'recover unsettled Oracle run',
  }, replayAgent)
  assert.equal(status.isError, false)

  await resumed.fiber.dispose()
})
