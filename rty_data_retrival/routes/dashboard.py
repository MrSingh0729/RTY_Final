from flask import Blueprint, render_template, request, send_file, jsonify, redirect, url_for
from flask_login import login_required
import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime
from utils.api import *
from utils.helpers import *
from config import Config
 
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
 
@dashboard_bp.route('/')
@login_required
def index():
    return render_template('index.html')
 
@dashboard_bp.route('/auto-data')
@login_required
def auto_data():
    try:
        token = get_token()
        projects = get_project_list(token)
        fpy_data = get_fpy(token, projects)
 
        desired_columns = ["project", "station", "inPut", "pass", "fail", "notFail", "der", "ntf", "rty"]
        filtered_data = [
            {col: row.get(col, "") for col in desired_columns}
            for row in fpy_data
        ]
 
        current_time = datetime.now().strftime("%H:%M")
        return render_template('dashboard/auto_data.html', data=filtered_data, current_time=current_time)
    except Exception as e:
        return render_template('errors/500.html', error=str(e))
 
@dashboard_bp.route('/project-specific', methods=['GET', 'POST'])
@login_required
def project_specific():
    try:
        token = get_token()
        projects = get_project_list(token)
        selected_project = None
        rty_goal = 90.0
        fpy_data = []
        failed_stations = []
        fail_details = []
 
        if request.method == 'POST':
            selected_project = request.form.get('project')
            rty_goal = float(request.form.get('rty_goal', 90.0))
            fpy_data_raw = get_fpy(token, [selected_project])
 
            desired_columns = ["project", "station", "inPut", "pass", "fail", "notFail", "der", "ntf", "rty"]
            fpy_data = [
                {col: row.get(col, "") for col in desired_columns}
                for row in fpy_data_raw
            ]
 
            if fpy_data and "rty" in fpy_data[0]:
                try:
                    actual_rty = float(str(fpy_data[0]["rty"]).replace("%", ""))
                    if actual_rty < rty_goal:
                        for row in fpy_data:
                            station = row.get("station")
                            ntf = float(str(row.get("ntf", "0")).replace("%", "")) if row.get("ntf") else None
                            der = float(str(row.get("der", "0")).replace("%", "")) if row.get("der") else None
 
                            if station in Config.NTF_GOALS and ntf is not None and ntf > Config.NTF_GOALS[station]:
                                failed_stations.append((station, "NTF", ntf, Config.NTF_GOALS[station]))
                                detail_data = get_station_ntf_details(token, selected_project, station)
                                detail_df = pd.DataFrame(detail_data)
                                detail_df = detail_df.rename(columns={
                                    "substation": "Computer Name",
                                    "sn": "SN",
                                    "symptomEnName": "Fault Description"
                                })
                                detail_df = detail_df[["SN", "Fault Description", "Computer Name"]]
 
                                top_computers = detail_df["Computer Name"].value_counts().head(3).to_dict()
                                top_faults_by_computer = {}
                                for comp in top_computers:
                                    comp_faults = detail_df[detail_df["Computer Name"] == comp]
                                    faults = comp_faults["Fault Description"].value_counts().head(3).reset_index().values.tolist()
                                    top_faults_by_computer[comp] = faults
 
                                fail_details.append({
                                    "station": station,
                                    "metric": "NTF",
                                    "actual": ntf,
                                    "goal": Config.NTF_GOALS[station],
                                    "top_computers": top_computers,
                                    "top_faults_by_computer": top_faults_by_computer
                                })
 
                            if station in Config.DER_GOALS and der is not None and der > Config.DER_GOALS[station]:
                                failed_stations.append((station, "DER", der, Config.DER_GOALS[station]))
                                detail_data = get_station_der_details(token, selected_project, station)
                                detail_df = pd.DataFrame(detail_data)
                                detail_df = detail_df.rename(columns={
                                    "sn": "SN",
                                    "responsibilityEnName": "Responsibility",
                                    "symptomEnName": "Symptoms"
                                })
                                detail_df = detail_df[["SN", "Responsibility", "Symptoms"]]
                                top_symptoms = get_top_n_counts(detail_df, "Symptoms", 3)
                                top_responsibilities = get_top_n_counts(detail_df, "Responsibility", 3)
 
                                fail_details.append({
                                    "station": station,
                                    "metric": "DER",
                                    "actual": der,
                                    "goal": Config.DER_GOALS[station],
                                    "top_symptoms": top_symptoms.to_dict(orient="records"),
                                    "top_responsibilities": top_responsibilities.to_dict(orient="records")
                                })
                except Exception as e:
                    print("RTY analysis error:", e)
 
        return render_template("dashboard/project_specific.html",
                               projects=projects,
                               selected_project=selected_project,
                               rty_goal=rty_goal,
                               data=fpy_data,
                               failed_stations=failed_stations,
                               fail_details=fail_details)
    except Exception as e:
        return render_template('errors/500.html', error=str(e))
 
@dashboard_bp.route('/model-specific', methods=['GET', 'POST'])
@login_required
def model_specific():
    try:
        token = get_token()
        selected_model = None
        station_type = "BE"
        start_date = None
        end_date = None
        rty_goal = 90.0
        fpy_data = []
        failed_stations = []
        fail_details = []
 
        if request.method == 'POST':
            selected_model = request.form.get('model_name')
            station_type = request.form.get('station_type', 'BE')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            rty_goal = float(request.form.get('rty_goal', 90.0))
 
            fpy_data_raw = get_fpy_by_model(token, selected_model, station_type, start_date, end_date)
 
            desired_columns = ["project", "station", "inPut", "pass", "fail", "notFail", "der", "ntf", "rty"]
            fpy_data = [
                {col: row.get(col, "") for col in desired_columns}
                for row in fpy_data_raw
            ]
 
            if fpy_data and "rty" in fpy_data[0]:
                try:
                    actual_rty = float(str(fpy_data[0]["rty"]).replace("%", ""))
                    if actual_rty < rty_goal:
                        for row in fpy_data:
                            station = row.get("station")
                            ntf = float(str(row.get("ntf", "0")).replace("%", "")) if row.get("ntf") else None
                            der = float(str(row.get("der", "0")).replace("%", "")) if row.get("der") else None
 
                            if station in Config.NTF_GOALS and ntf is not None and ntf > Config.NTF_GOALS[station]:
                                failed_stations.append((station, "NTF", ntf, Config.NTF_GOALS[station]))
                                detail_data = get_station_ntf_details_by_model(token, selected_model, station, station_type, start_date, end_date)
                                detail_df = pd.DataFrame(detail_data)
                                detail_df = detail_df.rename(columns={
                                    "substation": "Computer Name",
                                    "sn": "SN",
                                    "symptomEnName": "Fault Description"
                                })
                                detail_df = detail_df[["SN", "Fault Description", "Computer Name"]]
 
                                top_computers = detail_df["Computer Name"].value_counts().head(3).to_dict()
                                top_faults_by_computer = {}
                                for comp in top_computers:
                                    comp_faults = detail_df[detail_df["Computer Name"] == comp]
                                    faults = comp_faults["Fault Description"].value_counts().head(3).reset_index().values.tolist()
                                    top_faults_by_computer[comp] = faults
 
                                fail_details.append({
                                    "station": station,
                                    "metric": "NTF",
                                    "actual": ntf,
                                    "goal": Config.NTF_GOALS[station],
                                    "top_computers": top_computers,
                                    "top_faults_by_computer": top_faults_by_computer
                                })
 
                            if station in Config.DER_GOALS and der is not None and der > Config.DER_GOALS[station]:
                                failed_stations.append((station, "DER", der, Config.DER_GOALS[station]))
                                detail_data = get_station_der_details_by_model(token, selected_model, station, station_type, start_date, end_date)
                                detail_df = pd.DataFrame(detail_data)
                                detail_df = detail_df.rename(columns={
                                    "sn": "SN",
                                    "responsibilityEnName": "Responsibility",
                                    "symptomEnName": "Symptoms"
                                })
                                detail_df = detail_df[["SN", "Responsibility", "Symptoms"]]
                                top_symptoms = get_top_n_counts(detail_df, "Symptoms", 3)
                                top_responsibilities = get_top_n_counts(detail_df, "Responsibility", 3)
 
                                fail_details.append({
                                    "station": station,
                                    "metric": "DER",
                                    "actual": der,
                                    "goal": Config.DER_GOALS[station],
                                    "top_symptoms": top_symptoms.to_dict(orient="records"),
                                    "top_responsibilities": top_responsibilities.to_dict(orient="records")
                                })
                except Exception as e:
                    print("RTY analysis error:", e)
 
        return render_template("dashboard/model_specific.html",
                               selected_model=selected_model,
                               station_type=station_type,
                               start_date=start_date,
                               end_date=end_date,
                               rty_goal=rty_goal,
                               data=fpy_data,
                               failed_stations=failed_stations,
                               fail_details=fail_details)
    except Exception as e:
        return render_template('errors/500.html', error=str(e))
 
@dashboard_bp.route('/export-excel')
@login_required
def export_excel():
    project = request.args.get('project')
    rty_goal = float(request.args.get('rty_goal', 90.0))
 
    token = get_token()
    fpy_data_raw = get_fpy(token, [project])
 
    if not fpy_data_raw:
        return "No data to export."
 
    # Clean FPY table
    desired_columns = ["project", "station", "inPut", "pass", "fail", "notFail", "der", "ntf", "rty"]
    fpy_data = [{col: row.get(col, "") for col in desired_columns} for row in fpy_data_raw]
    fpy_df = pd.DataFrame(fpy_data).astype(str)
 
    failed_stations = []
    ntf_rows = []
    der_rows = []
 
    try:
        actual_rty = float(str(fpy_df["rty"].iloc[0]).replace("%", ""))
        if actual_rty < rty_goal:
            for _, row in fpy_df.iterrows():
                station = row["station"]
                ntf = float(str(row["ntf"]).replace("%", "")) if row["ntf"] else None
                der = float(str(row["der"]).replace("%", "")) if row["der"] else None
 
                if station in Config.NTF_GOALS and ntf > Config.NTF_GOALS[station]:
                    failed_stations.append((station, "NTF", ntf, Config.NTF_GOALS[station]))
                    detail_df = pd.DataFrame(get_station_ntf_details(token, project, station)).rename(columns={
                        "substation": "Computer Name",
                        "sn": "SN",
                        "symptomEnName": "Fault Description"
                    })[["SN", "Fault Description", "Computer Name"]]
 
                    top_computers = detail_df["Computer Name"].value_counts().head(3).to_dict()
                    for comp, count in top_computers.items():
                        faults = detail_df[detail_df["Computer Name"] == comp]["Fault Description"].value_counts().head(3)
                        fault_lines = [f"{i+1}. {fault} → {qty}" for i, (fault, qty) in enumerate(faults.items())]
                        ntf_rows.append([f"{comp} → {count}", "\n".join(fault_lines)])
 
                if station in Config.DER_GOALS and der > Config.DER_GOALS[station]:
                    failed_stations.append((station, "DER", der, Config.DER_GOALS[station]))
                    detail_df = pd.DataFrame(get_station_der_details(token, project, station)).rename(columns={
                        "sn": "SN",
                        "responsibilityEnName": "Responsibility",
                        "symptomEnName": "Symptoms"
                    })[["SN", "Responsibility", "Symptoms"]]
 
                    top_symptoms = detail_df["Symptoms"].value_counts().head(3)
                    top_responsibilities = detail_df["Responsibility"].value_counts().head(3)
 
                    for i in range(3):
                        symptom = top_symptoms.index[i] if i < len(top_symptoms) else ""
                        symptom_qty = top_symptoms.iloc[i] if i < len(top_symptoms) else ""
                        resp = top_responsibilities.index[i] if i < len(top_responsibilities) else ""
                        resp_qty = top_responsibilities.iloc[i] if i < len(top_responsibilities) else ""
                        der_rows.append([f"{symptom} → {symptom_qty}", f"{resp} → {resp_qty}"])
    except Exception as e:
        print("RTY analysis error:", e)
 
    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "FPY Report"
 
    bold = Font(bold=True)
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    header_fill = PatternFill(start_color="4361ee", end_color="4361ee", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
 
    def write_section(title, df_or_rows, headers=None):
        # Safely merge title row
        pre_row = ws.max_row if ws.max_row else 0
        ws.append([title])
        title_row = pre_row + 1
        ws.merge_cells(start_row=title_row, start_column=1, end_row=title_row, end_column=10)
        ws.cell(row=title_row, column=1).font = bold
 
        if isinstance(df_or_rows, pd.DataFrame):
            ws.append(list(df_or_rows.columns))
            for cell in ws[ws.max_row]:
                cell.font = header_font
                cell.alignment = center
                cell.fill = header_fill
            for row in df_or_rows.itertuples(index=False):
                ws.append(list(row))
        else:
            if headers:
                ws.append(headers)
                for cell in ws[ws.max_row]:
                    cell.font = header_font
                    cell.alignment = center
                    cell.fill = header_fill
            for row in df_or_rows:
                ws.append(row)
 
        ws.append([])  # Spacer row
 
    # Write FPY Table
    write_section("FPY Table", fpy_df)
 
    # Write Failed Stations
    if failed_stations:
        fail_df = pd.DataFrame(failed_stations, columns=["Station", "Metric", "Actual (%)", "Goal (%)"])
        write_section("Failed Stations", fail_df)
 
    # Write NTF Breakdown
    if ntf_rows:
        write_section("Top Failure Analysis — NTF", ntf_rows, ["Top Computer → Qty", "Top 3 Faults → Qty"])
 
    # Write DER Breakdown
    if der_rows:
        write_section("Top Failure Analysis — DER", der_rows, ["Symptom → Qty", "Responsibility → Qty"])
 
    # Adjust column width for 'project' column
    ws.column_dimensions['A'].width = 25  # Wider than others
 
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
 
    return send_file(output,
                     download_name=f"{project}_full_report.xlsx",
                     as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
 
@dashboard_bp.route('/export-pdf')
@login_required
def export_pdf():
    project = request.args.get('project')
    rty_goal = float(request.args.get('rty_goal', 90.0))
 
    token = get_token()
    fpy_data_raw = get_fpy(token, [project])
 
    if not fpy_data_raw:
        return "No data to export."
 
    # Clean FPY table
    desired_columns = ["project", "station", "inPut", "pass", "fail", "notFail", "der", "ntf", "rty"]
    fpy_data = [{col: row.get(col, "") for col in desired_columns} for row in fpy_data_raw]
    fpy_df = pd.DataFrame(fpy_data).astype(str)
 
    failed_stations = []
    ntf_blocks = []
    der_blocks = []
 
    try:
        actual_rty = float(str(fpy_df["rty"].iloc[0]).replace("%", ""))
        if actual_rty < rty_goal:
            for _, row in fpy_df.iterrows():
                station = row.get("station")
                ntf = float(str(row.get("ntf", "0")).replace("%", "")) if row.get("ntf") else None
                der = float(str(row.get("der", "0")).replace("%", "")) if row.get("der") else None
 
                if station in Config.NTF_GOALS and ntf is not None and ntf > Config.NTF_GOALS[station]:
                    failed_stations.append((station, "NTF", ntf, Config.NTF_GOALS[station]))
                    detail_data = get_station_ntf_details(token, project, station)
                    detail_df = pd.DataFrame(detail_data).rename(columns={
                        "substation": "Computer Name",
                        "sn": "SN",
                        "symptomEnName": "Fault Description"
                    })
                    detail_df = detail_df[["SN", "Fault Description", "Computer Name"]]
 
                    top_computers = detail_df["Computer Name"].value_counts().head(3).to_dict()
                    rows = ""
                    for comp, count in top_computers.items():
                        comp_faults = detail_df[detail_df["Computer Name"] == comp]
                        faults = comp_faults["Fault Description"].value_counts().head(3)
                        fault_lines = "".join([f"{i+1}. {fault} → {qty}<br>" for i, (fault, qty) in enumerate(faults.items())])
                        rows += f"<tr><td>{comp} → {count}</td><td>{fault_lines}</td></tr>"
                    ntf_blocks.append(f"""
                        <h3>{station} — NTF Analysis</h3>
                        <table>
                            <thead><tr><th>Top Computer → Qty</th><th>Top 3 Faults → Qty</th></tr></thead>
                            <tbody>{rows}</tbody>
                        </table>
                    """)
 
                if station in Config.DER_GOALS and der is not None and der > Config.DER_GOALS[station]:
                    failed_stations.append((station, "DER", der, Config.DER_GOALS[station]))
                    detail_df = pd.DataFrame(get_station_der_details(token, project, station)).rename(columns={
                        "sn": "SN",
                        "responsibilityEnName": "Responsibility",
                        "symptomEnName": "Symptoms"
                    })
                    detail_df = detail_df[["SN", "Responsibility", "Symptoms"]]
 
                    top_symptoms = detail_df["Symptoms"].value_counts().head(3)
                    top_responsibilities = detail_df["Responsibility"].value_counts().head(3)
 
                    rows = ""
                    for i in range(3):
                        symptom = top_symptoms.index[i] if i < len(top_symptoms) else ""
                        symptom_qty = top_symptoms.iloc[i] if i < len(top_symptoms) else ""
                        resp = top_responsibilities.index[i] if i < len(top_responsibilities) else ""
                        resp_qty = top_responsibilities.iloc[i] if i < len(top_responsibilities) else ""
                        rows += f"<tr><td>{symptom} → {symptom_qty}</td><td>{resp} → {resp_qty}</td></tr>"
                    der_blocks.append(f"""
                        <h3>{station} — DER Analysis</h3>
                        <table>
                            <thead><tr><th>Symptom → Qty</th><th>Responsibility → Qty</th></tr></thead>
                            <tbody>{rows}</tbody>
                        </table>
                    """)
    except Exception as e:
        print("RTY analysis error:", e)
 
    # Build FPY table manually with wider project column
    fpy_html = "<table border='1' cellspacing='0' cellpadding='4' style='width:100%;'>"
    fpy_html += "<thead><tr>"
    for col in fpy_df.columns:
        if col == "project":
            fpy_html += f"<th style='font-size:10px; white-space:normal; word-wrap:break-word; width:120px;'>{col}</th>"
        else:
            fpy_html += f"<th style='font-size:10px; white-space:normal; word-wrap:break-word;'>{col}</th>"
    fpy_html += "</tr></thead><tbody>"
 
    for _, row in fpy_df.iterrows():
        fpy_html += "<tr>"
        for col in fpy_df.columns:
            if col == "project":
                fpy_html += f"<td style='font-size:10px; white-space:normal; word-wrap:break-word; width:120px;'>{row[col]}</td>"
            else:
                fpy_html += f"<td style='font-size:10px; white-space:normal; word-wrap:break-word;'>{row[col]}</td>"
        fpy_html += "</tr>"
    fpy_html += "</tbody></table>"
 
    # Build full HTML
    html = f"""
    <html><head><style>
    body {{ font-family: Arial; font-size: 11px; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
    th, td {{ border: 1px solid #ccc; padding: 4px; text-align: left; vertical-align: top; }}
    th {{ background-color: #4361ee; color: white; }}
    h1 {{ margin-bottom: 10px; color: #4361ee; }}
    h2 {{ margin-top: 30px; color: #4361ee; }}
    h3 {{ margin-top: 20px; color: #4361ee; }}
    </style></head><body>
    <h1>FPY Report for {project}</h1>
    <p><strong>RTY Goal:</strong> {rty_goal}%</p>
 
    <h2>FPY Table</h2>
    {fpy_html}
    """
 
    if failed_stations:
        fail_df = pd.DataFrame(failed_stations, columns=["Station", "Metric", "Actual (%)", "Goal (%)"])
        html += "<h2>Failed Stations</h2>" + fail_df.to_html(index=False)
 
    if ntf_blocks or der_blocks:
        html += "<h2>Top Failure Analysis</h2>"
        html += "".join(ntf_blocks)
        html += "".join(der_blocks)
 
    html += "</body></html>"
 
    # Convert to PDF using ReportLab
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import inch
 
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    normal_style = styles['Normal']
    
    # Title
    elements.append(Paragraph(f"FPY Report for {project}", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"RTY Goal: {rty_goal}%", normal_style))
    elements.append(Spacer(1, 12))
    
    # FPY Table
    elements.append(Paragraph("FPY Table", heading_style))
    elements.append(Spacer(1, 12))
    
    # Convert DataFrame to list of lists for ReportLab
    fpy_data_list = [list(fpy_df.columns)] + fpy_df.values.tolist()
    fpy_table = Table(fpy_data_list)
    fpy_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(fpy_table)
    elements.append(Spacer(1, 12))
    
    # Failed Stations
    if failed_stations:
        elements.append(Paragraph("Failed Stations", heading_style))
        elements.append(Spacer(1, 12))
        
        failed_data = [["Station", "Metric", "Actual (%)", "Goal (%)"]] + failed_stations
        failed_table = Table(failed_data)
        failed_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(failed_table)
        elements.append(Spacer(1, 12))
    
    # NTF Breakdown
    if ntf_blocks:
        elements.append(Paragraph("Top Failure Analysis — NTF", heading_style))
        elements.append(Spacer(1, 12))
        
        for rows in ntf_blocks:
            ntf_table = Table([["Top Computer → Qty", "Top 3 Faults → Qty"]] + rows)
            ntf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(ntf_table)
            elements.append(Spacer(1, 12))
    
    # DER Breakdown
    if der_blocks:
        elements.append(Paragraph("Top Failure Analysis — DER", heading_style))
        elements.append(Spacer(1, 12))
        
        for rows in der_blocks:
            der_table = Table([["Symptom → Qty", "Responsibility → Qty"]] + rows)
            der_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(der_table)
            elements.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return send_file(buffer,
                     download_name=f"{project}_full_report.pdf",
                     as_attachment=True,
                     mimetype='application/pdf')