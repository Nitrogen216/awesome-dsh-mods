/** Keep automatic skill loading inside the curated dsh_autoresearch catalog. */

export const name = 'dsh-autoresearch-skill-isolation'
export const inject = ['tools']

/**
 * Register a final deny for skill-tool calls outside the preset allowlist.
 * Direct human /skill gestures remain human-owned overrides; the preset's
 * filesystem provider separately omits project and user discovery roots.
 */
export function apply(ctx, config = {}) {
  if (!Array.isArray(config.allowedSkills) || config.allowedSkills.length === 0) {
    throw new Error('skill-isolation: allowedSkills must be a non-empty array')
  }
  const allowed = new Set()
  for (const entry of config.allowedSkills) {
    if (typeof entry !== 'string' || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(entry)) {
      throw new Error('skill-isolation: every allowed skill must be a kebab-case name')
    }
    if (allowed.has(entry)) {
      throw new Error('skill-isolation: duplicate allowed skill ' + JSON.stringify(entry))
    }
    allowed.add(entry)
  }

  ctx.tools.guard(exec => {
    if (exec.name !== 'skill') return undefined
    const args = exec.arguments
    if (args === null || typeof args !== 'object' || Array.isArray(args)) {
      return 'dsh_autoresearch rejected a malformed skill request.'
    }
    const requested = args.name
    if (typeof requested !== 'string' || !allowed.has(requested)) {
      return 'dsh_autoresearch may load only its curated preset skills; external project and user skills are isolated.'
    }
    return undefined
  })
}
