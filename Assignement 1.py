
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

policyholders = []
claims = []

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Insurance Claims Management</title>
    <style>
        body {
            font-family: Arial;
            margin: 0;
            background: #f4f4f4;
        }
        h1 {
            background: #2c3e50;
            color: white;
            padding: 20px;
            margin: 0;
            text-align: center;
        }
        .container {
            display: flex;
        }
        .sidebar {
            background-color: #2c3e50;
            width: 220px;
            height: calc(100vh - 80px);
            padding-top: 20px;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
        }
        .sidebar button {
            display: block;
            background-color: transparent;
            color: white;
            border: none;
            width: 100%;
            padding: 15px;
            text-align: left;
            cursor: pointer;
            font-size: 16px;
        }
        .sidebar button:hover, .sidebar button.active {
            background-color: #34495e;
        }
        .content {
            flex-grow: 1;
            padding: 30px;
            background-color: white;
            height: calc(100vh - 80px);
            overflow-y: auto;
        }
        .tab-content {
            display: none;
        }
        .visible {
            display: block !important;
        }
        form {
            max-width: 600px;
        }
        label {
            display: block;
            margin-top: 10px;
            font-weight: bold;
        }
        input, select {
            padding: 10px;
            margin-top: 5px;
            width: 100%;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        input[type="submit"] {
            margin-top: 20px;
            background-color: #2ecc71;
            color: white;
            border: none;
        }
        input[type="submit"]:hover {
            background-color: #27ae60;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 10px;
        }
        th {
            background-color: #ecf0f1;
        }
    </style>
</head>
<body>

<h1>Insurance Claims Management System</h1>
<div class="container">
    <div class="sidebar">
        <button class="tab-button active" onclick="showTab('register')">➕ Register</button>
        <button class="tab-button" onclick="showTab('claim')">📝 Add Claim</button>
        <button class="tab-button" onclick="showTab('policyholders')">📋 Policyholders</button>
        <button class="tab-button" onclick="showTab('claims')">📄 Claims</button>
        <button class="tab-button" onclick="showTab('risk')">🚩 Risk Analysis</button>
    </div>
    <div class="content">
        <div id="register" class="tab-content visible">
            <h2>Register Policyholder</h2>
            <form method="post" action="/register">
                <label>Name:</label>
                <input type="text" name="name" required>
                <label>Age:</label>
                <input type="number" name="age" required>
                <label>Policy Type:</label>
                <select name="policy_type">
                    <option>Health</option>
                    <option>Vehicle</option>
                    <option>Life</option>
                </select>
                <label>Sum Insured:</label>
                <input type="number" name="sum_insured" required>
                <input type="submit" value="Register Policyholder">
            </form>
        </div>

        <div id="claim" class="tab-content">
            <h2>Add Claim</h2>
            <form method="post" action="/add_claim">
                <label>Policyholder ID:</label>
                <select name="policyholder_id" required>
                    {% for p in policyholders %}
                    <option value="{{ p['Policyholder ID'] }}">{{ p['Policyholder ID'] }} - {{ p['Name'] }}</option>
                    {% endfor %}
                </select>
                <label>Claim Amount:</label>
                <input type="number" name="claim_amount" required>
                <label>Reason:</label>
                <input type="text" name="reason" required>
                <label>Claim Status:</label>
                <select name="claim_status">
                    <option>Pending</option>
                    <option>Approved</option>
                    <option>Rejected</option>
                </select>
                <label>Date of Claim:</label>
                <input type="date" name="date_of_claim" required>
                <input type="submit" value="Submit Claim">
            </form>
        </div>

        <div id="policyholders" class="tab-content">
            <h2>Policyholders</h2>
            <table>
                <tr><th>ID</th><th>Name</th><th>Age</th><th>Policy Type</th><th>Sum Insured</th></tr>
                {% for p in policyholders %}
                <tr>
                    <td>{{ p['Policyholder ID'] }}</td>
                    <td>{{ p['Name'] }}</td>
                    <td>{{ p['Age'] }}</td>
                    <td>{{ p['Policy Type'] }}</td>
                    <td>{{ p['Sum Insured'] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div id="claims" class="tab-content">
            <h2>Claims</h2>
            <table>
                <tr><th>Claim ID</th><th>Policyholder ID</th><th>Amount</th><th>Reason</th><th>Status</th><th>Date</th></tr>
                {% for c in claims %}
                <tr>
                    <td>{{ c['Claim ID'] }}</td>
                    <td>{{ c['Policyholder ID'] }}</td>
                    <td>{{ c['Claim Amount'] }}</td>
                    <td>{{ c['Reason'] }}</td>
                    <td>{{ c['Claim Status'] }}</td>
                    <td>{{ c['Date of Claim'] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div id="risk" class="tab-content">
            <h2>High Risk Policyholders</h2>
            <table>
                <tr><th>ID</th><th>Name</th><th>Claims</th><th>Total Claimed</th><th>Sum Insured</th><th>Ratio</th><th>High Risk</th></tr>
                {% for r in risk %}
                <tr>
                    <td>{{ r['Policyholder ID'] }}</td>
                    <td>{{ r['Name'] }}</td>
                    <td>{{ r['Claims'] }}</td>
                    <td>{{ r['Total Claimed'] }}</td>
                    <td>{{ r['Sum Insured'] }}</td>
                    <td>{{ "%.2f" % r['Claim Ratio'] }}</td>
                    <td>{{ "Yes" if r['High Risk'] else "No" }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
</div>

<script>
    function showTab(tabId) {
        var tabs = document.getElementsByClassName("tab-content");
        var buttons = document.getElementsByClassName("tab-button");
        for (var i = 0; i < tabs.length; i++) {
            tabs[i].classList.remove("visible");
            buttons[i].classList.remove("active");
        }
        document.getElementById(tabId).classList.add("visible");
        event.currentTarget.classList.add("active");
    }
</script>

</body>
</html>
'''

def calculate_risk():
    from collections import defaultdict
    claim_counts = defaultdict(int)
    total_claimed = defaultdict(float)
    result = []

    for claim in claims:
        pid = claim['Policyholder ID']
        claim_counts[pid] += 1
        total_claimed[pid] += float(claim['Claim Amount'])

    for holder in policyholders:
        pid = holder['Policyholder ID']
        claim_count = claim_counts.get(pid, 0)
        total = total_claimed.get(pid, 0.0)
        sum_insured = float(holder['Sum Insured'])
        ratio = total / sum_insured if sum_insured else 0
        high_risk = claim_count > 3 or ratio > 0.8
        result.append({
            'Policyholder ID': pid,
            'Name': holder['Name'],
            'Claims': claim_count,
            'Total Claimed': total,
            'Sum Insured': sum_insured,
            'Claim Ratio': ratio,
            'High Risk': high_risk
        })
    return result

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, policyholders=policyholders, claims=claims, risk=calculate_risk())

@app.route('/register', methods=['POST'])
def register():
    policyholder_id = f"PH{len(policyholders)+1:04d}"
    policyholders.append({
        "Policyholder ID": policyholder_id,
        "Name": request.form['name'],
        "Age": int(request.form['age']),
        "Policy Type": request.form['policy_type'],
        "Sum Insured": float(request.form['sum_insured'])
    })
    return redirect(url_for('index'))

@app.route('/add_claim', methods=['POST'])
def add_claim():
    claim_id = f"CLM{len(claims)+1:05d}"
    claims.append({
        "Claim ID": claim_id,
        "Policyholder ID": request.form['policyholder_id'],
        "Claim Amount": float(request.form['claim_amount']),
        "Reason": request.form['reason'],
        "Claim Status": request.form['claim_status'],
        "Date of Claim": request.form['date_of_claim']
    })
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
