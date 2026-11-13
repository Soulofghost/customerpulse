const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initModal();
  initSimulator();
  loadStats();
  loadCustomers();
});

function initTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      tab.classList.add('active');
      const target = tab.dataset.tab === 'accounts' ? 'paneAccounts' : 'paneSimulator';
      document.getElementById(target)?.classList.add('active');
    });
  });
}

function initModal() {
  const modal = document.getElementById('custModal');
  const openBtn = document.getElementById('openCustModal');
  const closeBtn = document.getElementById('closeCustBtn');
  const cancelBtn = document.getElementById('cancelCustBtn');
  const form = document.getElementById('createCustForm');

  openBtn?.addEventListener('click', () => modal.classList.add('active'));
  closeBtn?.addEventListener('click', () => modal.classList.remove('active'));
  cancelBtn?.addEventListener('click', () => modal.classList.remove('active'));

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const customer_name = document.getElementById('custName').value.trim();
    const email = document.getElementById('custEmail').value.trim();
    const company = document.getElementById('custCompany').value.trim();

    try {
      const res = await fetch(`${API_BASE}/customers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_name,
          email,
          company,
          plan_tier: 'Enterprise',
          tenure_months: 14,
          monthly_spend: 850.0,
          inactivity_days: 4,
          support_tickets: 1,
          contract_type: 'Annual',
          feature_usage_score: 80.0
        })
      });

      if (!res.ok) throw new Error('Failed to register customer');
      modal.classList.remove('active');
      form.reset();
      await loadStats();
      await loadCustomers();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  });
}

function initSimulator() {
  const simTenure = document.getElementById('simTenure');
  const simInactivity = document.getElementById('simInactivity');
  const simTickets = document.getElementById('simTickets');
  const simUsage = document.getElementById('simUsage');
  const simContract = document.getElementById('simContract');
  const runBtn = document.getElementById('runSimBtn');

  simTenure?.addEventListener('input', () => {
    document.getElementById('tenureVal').innerText = `${simTenure.value} Months`;
    runSimulation();
  });

  simInactivity?.addEventListener('input', () => {
    document.getElementById('inactivityVal').innerText = `${simInactivity.value} Days`;
    runSimulation();
  });

  simTickets?.addEventListener('input', () => {
    document.getElementById('ticketsVal').innerText = `${simTickets.value} Ticket(s)`;
    runSimulation();
  });

  simUsage?.addEventListener('input', () => {
    document.getElementById('usageVal').innerText = `${simUsage.value} / 100`;
    runSimulation();
  });

  simContract?.addEventListener('change', runSimulation);
  runBtn?.addEventListener('click', runSimulation);

  // Initial trigger
  runSimulation();
}

async function runSimulation() {
  const contract_type = document.getElementById('simContract').value;
  const tenure_months = parseInt(document.getElementById('simTenure').value, 10);
  const inactivity_days = parseInt(document.getElementById('simInactivity').value, 10);
  const support_tickets = parseInt(document.getElementById('simTickets').value, 10);
  const feature_usage_score = parseFloat(document.getElementById('simUsage').value);

  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer_name: 'Simulated Entity',
        email: 'sim@entity.com',
        company: 'Simulation Inc',
        tenure_months,
        monthly_spend: 499.0,
        inactivity_days,
        support_tickets,
        contract_type,
        feature_usage_score
      })
    });

    if (!res.ok) throw new Error('Simulation failed');
    const data = await res.json();
    renderSimulationResults(data);
  } catch (err) {
    console.warn(err);
  }
}

function renderSimulationResults(data) {
  const probEl = document.getElementById('simProbability');
  probEl.innerText = `${data.risk_percentage}%`;
  probEl.style.color = data.risk_tier === 'LOW' ? 'var(--accent-emerald)' : data.risk_tier === 'MEDIUM' ? 'var(--accent-amber)' : 'var(--accent-red)';

  const badge = document.getElementById('simRiskBadge');
  badge.innerText = `RISK: ${data.risk_tier}`;
  badge.className = `badge badge-${data.risk_tier.toLowerCase()}`;

  document.getElementById('simRecommendation').innerHTML = `<strong>Recommended Playbook:</strong> ${data.recommended_action}`;

  const impactList = document.getElementById('simImpactList');
  impactList.innerHTML = data.feature_contributions.map(c => `
    <div class="impact-item">
      <div>
        <strong>${c.feature}</strong> <span class="text-mono" style="font-size:0.75rem; color:var(--text-secondary);">(${c.value})</span>
      </div>
      <div style="font-weight:700; color: ${c.direction === 'RISK_INCREASE' ? 'var(--accent-red)' : c.direction === 'RISK_REDUCTION' ? 'var(--accent-emerald)' : 'var(--text-secondary)'}">
        ${c.impact > 0 ? `+${c.impact}` : c.impact}
      </div>
    </div>
  `).join('');
}

async function loadStats() {
  try {
    const res = await fetch(`${API_BASE}/stats`);
    const data = await res.json();
    document.getElementById('statCustomers').innerText = data.totalCustomers;
    document.getElementById('statAtRisk').innerText = data.atRiskAccounts;
    document.getElementById('statAvgRisk').innerText = `${data.averageChurnRisk}%`;
    document.getElementById('statMrrRisk').innerText = `$${data.monthlyRevenueAtRisk.toLocaleString(undefined, {minimumFractionDigits: 2})}`;
  } catch (err) {
    console.warn('Failed to load stats', err);
  }
}

async function loadCustomers() {
  const tbody = document.getElementById('customersTableBody');
  try {
    const res = await fetch(`${API_BASE}/customers`);
    const list = await res.json();

    if (!list || list.length === 0) {
      // Seed initial accounts
      const seedAccounts = [
        { customer_name: "Marcus Vance", email: "mvance@vanguard.io", company: "Vanguard Tech", plan_tier: "Enterprise", tenure_months: 28, monthly_spend: 1800.0, inactivity_days: 2, support_tickets: 0, contract_type: "Annual", feature_usage_score: 92.0 },
        { customer_name: "Elena Rostova", email: "elena@novacorp.de", company: "Nova Logistics", plan_tier: "Growth", tenure_months: 4, monthly_spend: 350.0, inactivity_days: 21, support_tickets: 3, contract_type: "Month-to-Month", feature_usage_score: 28.0 },
        { customer_name: "David Kim", email: "dkim@solaris.co", company: "Solaris Media", plan_tier: "Scale", tenure_months: 11, monthly_spend: 650.0, inactivity_days: 8, support_tickets: 1, contract_type: "Month-to-Month", feature_usage_score: 62.0 },
        { customer_name: "Chloe Bennett", email: "chloe@apexfin.com", company: "Apex Financial", plan_tier: "Enterprise", tenure_months: 3, monthly_spend: 1200.0, inactivity_days: 29, support_tickets: 5, contract_type: "Month-to-Month", feature_usage_score: 12.0 }
      ];

      for (const a of seedAccounts) {
        await fetch(`${API_BASE}/customers`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(a)
        });
      }
      return loadCustomers();
    }

    tbody.innerHTML = list.map(c => `
      <tr>
        <td><span class="badge badge-${c.risk_tier.toLowerCase()}">${c.risk_tier}</span></td>
        <td><strong>${escapeHtml(c.customer_name)}</strong></td>
        <td>${escapeHtml(c.company)}</td>
        <td><span class="badge badge-info">${c.plan_tier}</span></td>
        <td>${c.tenure_months} mo</td>
        <td class="text-mono">$${c.monthly_spend.toFixed(0)}</td>
        <td>${c.inactivity_days} d</td>
        <td>${c.support_tickets}</td>
        <td>${c.feature_usage_score}/100</td>
        <td><strong style="color: ${c.risk_tier === 'LOW' ? 'var(--accent-emerald)' : c.risk_tier === 'MEDIUM' ? 'var(--accent-amber)' : 'var(--accent-red)'}">${(c.churn_probability * 100).toFixed(1)}%</strong></td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="10" style="color: var(--accent-red); padding: 1rem;">Failed to load accounts: ${err.message}</td></tr>`;
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
