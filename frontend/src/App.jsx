import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

import {
  Activity,
  ArrowRight,
  Bot,
  BriefcaseBusiness,
  CheckCircle2,
  Circle,
  Clock3,
  FileText,
  LayoutDashboard,
  LoaderCircle,
  Sparkles,
  Wallet,
  Workflow,
  XCircle,
} from 'lucide-react'

const agents = [
  'Business Analyst',
  'Solution Architect',
  'Cost Analyst',
  'Project Planner',
  'Critic Agent',
]


const initialForm = {
  business_name: '',
  industry: '',
  industry_domain: 'other',
  business_description: '',
  business_problem: '',
  budget_amount: '',
  currency: 'INR',
  budget_scope: 'initial_only',
  business_size: 'Small Business',
}


function App() {
  const [form, setForm] = useState(initialForm)
  const [loading, setLoading] = useState(false)
  const [report, setReport] = useState(null)
  const [logs, setLogs] = useState([])
  const [error, setError] = useState('')

  const updateField = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value })
  }
  

  const runAnalysis = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    setReport(null)
    setLogs([])

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Analysis failed. Please try again.')
      }

      setReport(data.report)
      setLogs(data.agent_logs || [])
    } catch (err) {
      setError(
        err.message === 'Failed to fetch'
          ? 'Cannot connect to BizPilot backend. Check that FastAPI is running on port 8000.'
          : err.message
      )
    } finally {
      setLoading(false)
    }
  }

  const reportSections = report
    ? [
        ['Business Analysis', report.business_analysis?.analysis, BriefcaseBusiness],
        ['Solution Architecture', report.solution?.solution, Workflow],
        ['Cost Analysis', report.cost_analysis?.financial_analysis, Wallet],
        ['Project Roadmap', report.project_roadmap?.roadmap, Activity],
        ['Critic Review', report.critic_review?.review, CheckCircle2],
      ]
    : []

  return (
    <div className="min-h-screen bg-[#09090f] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden w-64 shrink-0 border-r border-white/10 bg-[#0d0d16] p-6 md:flex md:flex-col">
          <div className="mb-12 flex items-center gap-3">
            <div className="rounded-xl bg-violet-600 p-2.5">
              <Bot size={24} />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-wide">BizPilot</h1>
              <p className="text-xs text-zinc-500">AI Business Consultant</p>
            </div>
          </div>

          <p className="mb-3 text-xs font-semibold uppercase tracking-widest text-zinc-600">
            Workspace
          </p>

          <div className="flex items-center gap-3 rounded-xl border border-violet-500/20 bg-violet-500/10 px-4 py-3 text-sm text-violet-300">
            <LayoutDashboard size={18} />
            Dashboard
          </div>

          <div className="mt-3 flex items-center gap-3 px-4 py-3 text-sm text-zinc-500">
            <FileText size={18} />
            Business Reports
            <span className="ml-auto text-xs">Soon</span>
          </div>

          <div className="mt-3 flex items-center gap-3 px-4 py-3 text-sm text-zinc-500">
            <Workflow size={18} />
            Agent Workflow
          </div>

          <div className="mt-auto rounded-2xl border border-white/10 bg-white/[0.03] p-4">
            <div className="mb-2 flex items-center gap-2 text-sm font-medium">
              <Sparkles size={16} className="text-violet-400" />
              Powered by AI
            </div>
            <p className="text-xs leading-5 text-zinc-500">
              Five specialist agents working together to solve business problems.
            </p>
          </div>
        </aside>

        <main className="min-w-0 flex-1">
          <header className="flex items-center justify-between border-b border-white/10 px-5 py-5 md:px-10">
            <div>
              <p className="text-sm text-zinc-500">Workspace / Dashboard</p>
              <h2 className="mt-1 text-lg font-semibold">Business Intelligence</h2>
            </div>
            <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-xs text-emerald-400">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              AI Engine Ready
            </div>
          </header>

          <div className="mx-auto max-w-6xl p-5 md:p-10">
            <section className="relative mb-8 overflow-hidden rounded-3xl border border-violet-500/20 bg-gradient-to-br from-violet-950/70 via-[#171326] to-[#10101b] p-7 md:p-10">
              <div className="pointer-events-none absolute -right-16 -top-24 h-72 w-72 rounded-full bg-violet-600/20 blur-3xl" />
              <div className="relative max-w-2xl">
                <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-violet-400/20 bg-violet-400/10 px-3 py-1.5 text-xs text-violet-300">
                  <Sparkles size={14} />
                  Multi-Agent Business Intelligence
                </div>
                <h1 className="text-3xl font-bold leading-tight md:text-4xl">
                  Turn business problems into
                  <span className="text-violet-400"> intelligent solutions.</span>
                </h1>
                <p className="mt-4 max-w-xl text-sm leading-6 text-zinc-400">
                  Describe your business challenge. BizPilot's five AI specialists
                  will analyze it, design a solution, estimate costs and create an
                  implementation roadmap.
                </p>
              </div>
            </section>

            <div className="mb-6 grid gap-4 sm:grid-cols-3">
              <StatCard icon={Bot} label="AI Specialists" value="05" />
              <StatCard icon={Workflow} label="Workflow Engine" value="LangGraph" />
              <StatCard icon={Activity} label="Analysis Status" value={loading ? 'Running' : report ? 'Completed' : 'Ready'} />
            </div>

            <div className="grid items-start gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <section className="rounded-2xl border border-white/10 bg-[#11111b] p-6">
                <div className="mb-6">
                  <p className="text-xs font-semibold uppercase tracking-widest text-violet-400">
                    New analysis
                  </p>
                  <h2 className="mt-2 text-xl font-semibold">Tell us about your business</h2>
                  <p className="mt-2 text-sm text-zinc-500">
                    Provide the details below to generate your business report.
                  </p>
                </div>

                <form onSubmit={runAnalysis} className="space-y-5">
                  <div>
                    <FieldLabel>Business Name</FieldLabel>
                    <input
                      required
                      minLength={2}
                      name="business_name"
                      value={form.business_name}
                      onChange={updateField}
                      placeholder="e.g. GlowUp Salon"
                      className="field"
                      
                    />
                  </div>

                  
                  <div>
                    <FieldLabel>Industry Name</FieldLabel>
                    <input
                      required
                      name="industry"
                      value={form.industry}
                      onChange={updateField}
                      placeholder="e.g. Water and Sanitation"
                      className="field"
                    />
                  </div>

                  <div>
                    <FieldLabel>Industry Category</FieldLabel>
                    <select
                      name="industry_domain"
                      value={form.industry_domain}
                      onChange={updateField}
                      className="field"
                    >
                      <option value="retail">Retail and E-commerce</option>
                      <option value="beauty">Beauty and Wellness</option>
                      <option value="food">Food and Restaurants</option>
                      <option value="healthcare">Healthcare</option>
                      <option value="education">Education</option>
                      <option value="manufacturing">Manufacturing</option>
                      <option value="water">Water and Sanitation</option>
                      <option value="agriculture">Agriculture</option>
                      <option value="hospitality">Hospitality and Tourism</option>
                      <option value="logistics">Logistics</option>
                      <option value="professional">Professional Services</option>
                      <option value="other">Other</option>
                    </select>
                  </div>


                  <div>
                    <FieldLabel>Business Description</FieldLabel>
                    <textarea
                      required
                      minLength={10}
                      rows={3}
                      name="business_description"
                      value={form.business_description}
                      onChange={updateField}
                      placeholder="Describe your business, customers and current operations..."
                      className="field resize-y"
                    />
                  </div>

                  <div>
                    <FieldLabel>Business Problem</FieldLabel>
                    <textarea
                      required
                      minLength={10}
                      rows={4}
                      name="business_problem"
                      value={form.business_problem}
                      onChange={updateField}
                      placeholder="What problems or challenges do you want to solve?"
                      className="field resize-y"
                    />
                  </div>

                  
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div>
                      <FieldLabel>Available Budget</FieldLabel>
                      <input
                        required
                        type="number"
                        min="1"
                        name="budget_amount"
                        value={form.budget_amount}
                        onChange={updateField}
                        placeholder="e.g. 30000"
                        className="field"
                      />
                    </div>

                  <div>
                    <FieldLabel>Currency</FieldLabel>
                    <select
                      name="currency"
                      value={form.currency}
                      onChange={updateField}
                      className="field"
                    >
                      <option value="INR">INR (₹)</option>
                      <option value="USD">USD ($)</option>
                      <option value="EUR">EUR (€)</option>
                      <option value="GBP">GBP (£)</option>
                    </select>
                  </div>
                  {/* Budget Scope */}
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Budget Coverage
                    </label>

                    <select
                      name="budget_scope"
                      value={form.budget_scope}
                      onChange={updateField}
                      className="w-full rounded-lg border border-white/10
                      bg-slate-900 px-4 py-3 text-white
                      focus:outline-none focus:ring-2 focus:ring-violet-500"
                    >
                      <option value="initial_only">
                        Initial Implementation Only
                      </option>

                      <option value="first_year_total">
                        Complete First-Year Budget
                      </option>
                    </select>

                    <p className="text-xs text-gray-400 mt-2">
                      Choose whether your budget covers only setup costs
                      or setup plus 12 months of operating expenses.
                    </p>
                  </div>

                  

                  <div className="sm:col-span-2">
                    <FieldLabel>Business Size</FieldLabel>
                    <select
                      name="business_size"
                      value={form.business_size}
                      onChange={updateField}
                      className="field"
                    >
                      <option>Startup</option>
                      <option>Small Business</option>
                      <option>Medium Business</option>
                      <option>Enterprise</option>
                    </select>
                  </div>
                </div>

                    

                  {error && (
                    <div className="flex gap-2 rounded-xl border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-300">
                      <XCircle size={18} className="shrink-0" />
                      {error}
                    </div>
                  )}

                  <button
                    disabled={loading}
                    type="submit"
                    className="flex w-full items-center justify-center gap-2 rounded-xl bg-violet-600 px-5 py-3.5 font-semibold transition hover:bg-violet-500 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {loading ? (
                      <>
                        <LoaderCircle size={18} className="animate-spin" />
                        AI Agents Analysing...
                      </>
                    ) : (
                      <>
                        Generate Business Analysis
                        <ArrowRight size={18} />
                      </>
                    )}
                  </button>
                </form>
              </section>

              <section className="rounded-2xl border border-white/10 bg-[#11111b] p-6">
                <div className="mb-6">
                  <p className="text-xs font-semibold uppercase tracking-widest text-cyan-400">
                    Agent orchestration
                  </p>
                  <h2 className="mt-2 text-xl font-semibold">Your AI team</h2>
                  <p className="mt-2 text-sm text-zinc-500">
                    Five specialists collaborate in a sequential workflow.
                  </p>
                </div>

                <div className="space-y-3">
                  {agents.map((agent, index) => {
                    const completed = logs.some(
                      (log) => log.agent === agent && log.status === 'completed'
                    )

                    return (
                      <div key={agent} className="flex items-center gap-3 rounded-xl border border-white/[0.07] bg-white/[0.02] p-4">
                        <div className={`rounded-lg p-2 ${completed ? 'bg-emerald-500/10 text-emerald-400' : 'bg-violet-500/10 text-violet-300'}`}>
                          {completed ? <CheckCircle2 size={19} /> : <Circle size={19} />}
                        </div>
                        <div className="min-w-0 flex-1">
                          <p className="text-sm font-medium">{agent}</p>
                          <p className="mt-1 text-xs text-zinc-500">
                            {completed ? 'Completed successfully' : `Specialist ${index + 1}`}
                          </p>
                        </div>
                        {completed && (
                          <span className="text-xs text-emerald-400">Done</span>
                        )}
                      </div>
                    )
                  })}
                </div>

                <div className="mt-5 rounded-xl border border-white/[0.07] bg-black/20 p-4">
                  <div className="flex items-center gap-2 text-sm text-zinc-400">
                    <Clock3 size={16} />
                    Workflow execution
                  </div>
                  <p className="mt-2 text-sm text-zinc-500">
                    {loading
                      ? 'The backend is processing your request. Agent updates will appear after the response is received.'
                      : report
                        ? 'All five agents have returned their results.'
                        : 'Submit a business problem to start the workflow.'}
                  </p>
                </div>
              </section>
            </div>

            {report && (
              <section className="mt-8 space-y-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-widest text-emerald-400">
                      Analysis complete
                    </p>
                    <h2 className="mt-1 text-2xl font-bold">Business Intelligence Report</h2>
                    <p className="mt-1 text-sm text-zinc-500">
                      {report.business_name} · {report.industry}
                    </p>
                  </div>
                  <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-2 text-xs text-emerald-400">
                    {logs.filter(log =>
                      agents.includes(log.agent) &&
                      log.status === 'completed'
                    ).length} / 5 agents completed
                  </span>
                </div>

                {reportSections.map(([title, content, Icon]) => (
                  <article key={title} className="rounded-2xl border border-white/10 bg-[#11111b] p-6">
                    <div className="mb-4 flex items-center gap-3">
                      <div className="rounded-lg bg-violet-500/10 p-2 text-violet-300">
                        <Icon size={20} />
                      </div>
                      <h3 className="font-semibold">{title}</h3>
                    </div>
                    <div className="
                      break-words text-sm leading-7 text-zinc-300
                      [&_h1]:mb-4 [&_h1]:text-xl [&_h1]:font-bold [&_h1]:text-white
                      [&_h2]:mb-3 [&_h2]:mt-6 [&_h2]:text-lg [&_h2]:font-semibold [&_h2]:text-white
                      [&_h3]:mb-2 [&_h3]:mt-4 [&_h3]:font-semibold [&_h3]:text-white
                      [&_strong]:font-semibold [&_strong]:text-white
                      [&_ul]:my-3 [&_ul]:list-disc [&_ul]:pl-6
                      [&_ol]:my-3 [&_ol]:list-decimal [&_ol]:pl-6
                      [&_li]:my-1
                      [&_table]:my-4 [&_table]:w-full [&_table]:border-collapse
                      [&_th]:border [&_th]:border-white/10 [&_th]:bg-white/5 [&_th]:p-2 [&_th]:text-left [&_th]:text-white
                      [&_td]:border [&_td]:border-white/10 [&_td]:p-2
                      [&_blockquote]:my-3 [&_blockquote]:border-l-2 [&_blockquote]:border-violet-500 [&_blockquote]:pl-4
                    ">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {(content || 'No information returned for this section.')
                          .replace(/<br\s*\/?>/gi, '\n')
                          .replace(/\\([*_#>|`])/g, '$1')}
                      </ReactMarkdown>
                    </div>
                  </article>
                ))}
              </section>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

function FieldLabel({ children }) {
  return (
    <label className="mb-2 block text-sm font-medium text-zinc-300">
      {children}
    </label>
  )
}

function StatCard({ icon: Icon, label, value }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#11111b] p-5">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm text-zinc-500">{label}</p>
        <Icon size={18} className="text-violet-400" />
      </div>
      <p className="text-xl font-semibold">{value}</p>
    </div>
  )
}

export default App