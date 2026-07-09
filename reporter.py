import os
import json

def save_reports(analysis_data, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    
    json_path = os.path.join(output_dir, "analysis.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    md_path = os.path.join(output_dir, "report.md")
    md_content = f"# Repository Analysis Report\n\n"
    md_content += f"## Summary\n{analysis_data.get('summary', 'No summary provided.')}\n\n"
    
    md_content += "## Technologies Used\n"
    for tech in analysis_data.get('technologies', []):
        md_content += f"- {tech}\n"
        
    md_content += "\n## Strengths (Сильні сторони)\n"
    strengths = analysis_data.get('strengths', [])
    if strengths:
        for strength in strengths:
            md_content += f"- 💪 {strength}\n"
    else:
        md_content += "- No explicit strengths highlighted.\n"
        
    md_content += "\n## Identified Issues\n"
    for issue in analysis_data.get('issues', []):
        md_content += f"- ⚠️ {issue}\n"
        
    md_content += "\n## Recommendations\n"
    for rec in analysis_data.get('recommendations', []):
        md_content += f"- 💡 {rec}\n"
        
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

def save_pr_review(review_data, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    
    json_path = os.path.join(output_dir, "pr_review.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(review_data, f, indent=2, ensure_ascii=False)
        
    md_path = os.path.join(output_dir, "pr_review.md")
    status = "🟢 APPROVED" if review_data.get("approved", True) else "🔴 NEEDS CHANGES"
    
    md_content = f"# Pull Request Review Report (Bonus Task)\n\n"
    md_content += f"**Status:** {status}\n\n"
    md_content += f"## Summary of Changes\n{review_data.get('summary', 'No summary provided.')}\n\n"
    
    md_content += "## Potential Bugs & Edge Cases\n"
    bugs = review_data.get('bugs', [])
    if bugs:
        for bug in bugs:
            md_content += f"- 🐛 {bug}\n"
    else:
        md_content += "- No obvious bugs or edge cases found.\n"
        
    md_content += "\n## Style & Architecture Remarks\n"
    remarks = review_data.get('style_and_architecture', [])
    if remarks:
        for remark in remarks:
            md_content += f"- 🎨 {remark}\n"
    else:
        md_content += "- Code style and architecture look solid.\n"
        
    md_content += "\n## Optimization Proposals\n"
    opts = review_data.get('optimization', [])
    if opts:
        for opt in opts:
            md_content += f"- ⚡ {opt}\n"
    else:
        md_content += "- No explicit optimization suggestions needed.\n"
        
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
