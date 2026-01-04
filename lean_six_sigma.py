"""
MVAI Connexx - Lean Six Sigma DMAIC Framework
Process optimization en continuous improvement methodologie
"""
import json
from typing import Dict, List, Optional
from enum import Enum
import database as db
from collections import defaultdict
import statistics

# ═══════════════════════════════════════════════════════
# LEAN SIX SIGMA CONSTANTS
# ═══════════════════════════════════════════════════════

class DMAICPhase(Enum):
    """DMAIC methodology phases"""
    DEFINE = "define"          # Define problem en project goals
    MEASURE = "measure"        # Measure current process performance
    ANALYZE = "analyze"        # Analyze root causes
    IMPROVE = "improve"        # Implement improvements
    CONTROL = "control"        # Control en sustain improvements

class DefectType(Enum):
    """Types of defects/issues"""
    DATA_QUALITY = "data_quality"          # Incomplete/incorrect data
    PERFORMANCE = "performance"            # Slow response times
    AVAILABILITY = "availability"          # System downtime
    SECURITY = "security"                  # Security incidents
    USER_ERROR = "user_error"              # User-reported errors
    API_ERROR = "api_error"                # API failures

class ProcessMetric(Enum):
    """Key process metrics"""
    DEFECTS_PER_MILLION = "dpm"           # Defects Per Million Opportunities
    CYCLE_TIME = "cycle_time"              # Time to complete process
    THROUGHPUT = "throughput"              # Items processed per time unit
    FIRST_PASS_YIELD = "fpy"              # % correct first time
    CUSTOMER_SATISFACTION = "csat"         # Customer satisfaction score

# ═══════════════════════════════════════════════════════
# SIX SIGMA QUALITY CALCULATOR
# ═══════════════════════════════════════════════════════

class SixSigmaCalculator:
    """Calculate Six Sigma quality metrics"""

    # Sigma levels (defects per million opportunities)
    SIGMA_LEVELS = {
        6: 3.4,
        5: 233,
        4: 6210,
        3: 66807,
        2: 308537,
        1: 690000
    }

    def calculate_sigma_level(self, defects: int, opportunities: int) -> Dict:
        """
        Calculate current Sigma level

        Args:
            defects: Number of defects found
            opportunities: Total opportunities for defects

        Returns:
            Sigma level and DPM (Defects Per Million)
        """
        if opportunities == 0:
            return {
                'sigma_level': 6.0,
                'dpm': 0,
                'quality_percentage': 100.0,
                'grade': 'World Class'
            }

        # Calculate Defects Per Million Opportunities
        dpm = (defects / opportunities) * 1000000

        # Determine sigma level
        sigma_level = 1.0
        for level, threshold in sorted(self.SIGMA_LEVELS.items(), reverse=True):
            if dpm <= threshold:
                sigma_level = float(level)
                break

        # Quality percentage
        quality_pct = ((opportunities - defects) / opportunities) * 100

        # Grade
        if sigma_level >= 6:
            grade = 'World Class (6σ)'
        elif sigma_level >= 5:
            grade = 'Excellent (5σ)'
        elif sigma_level >= 4:
            grade = 'Good (4σ)'
        elif sigma_level >= 3:
            grade = 'Average (3σ)'
        elif sigma_level >= 2:
            grade = 'Below Average (2σ)'
        else:
            grade = 'Poor (1σ)'

        return {
            'sigma_level': sigma_level,
            'dpm': round(dpm, 2),
            'quality_percentage': round(quality_pct, 4),
            'grade': grade,
            'defects': defects,
            'opportunities': opportunities
        }

    def calculate_process_capability(self, values: List[float], spec_lower: float, spec_upper: float) -> Dict:
        """
        Calculate Process Capability (Cp, Cpk)

        Cp = (USL - LSL) / (6 * σ)
        Cpk = min((USL - μ) / (3 * σ), (μ - LSL) / (3 * σ))
        """
        if not values or len(values) < 2:
            return {'cp': None, 'cpk': None, 'capable': False}

        mean = statistics.mean(values)
        std_dev = statistics.stdev(values)

        if std_dev == 0:
            return {'cp': float('inf'), 'cpk': float('inf'), 'capable': True}

        # Process Capability
        cp = (spec_upper - spec_lower) / (6 * std_dev)

        # Process Capability Index
        cpk_upper = (spec_upper - mean) / (3 * std_dev)
        cpk_lower = (mean - spec_lower) / (3 * std_dev)
        cpk = min(cpk_upper, cpk_lower)

        # Process is capable if Cpk >= 1.33
        capable = cpk >= 1.33

        return {
            'cp': round(cp, 3),
            'cpk': round(cpk, 3),
            'capable': capable,
            'mean': round(mean, 2),
            'std_dev': round(std_dev, 2),
            'grade': 'Capable' if capable else 'Not Capable'
        }

# Global calculator
sigma_calculator = SixSigmaCalculator()

# ═══════════════════════════════════════════════════════
# DMAIC PROJECT MANAGER
# ═══════════════════════════════════════════════════════

class DMAICProject:
    """Manage DMAIC improvement projects"""

    def __init__(self, project_id: Optional[int] = None):
        self.project_id = project_id
        if project_id:
            self._load_project()

    def _load_project(self):
        """Load project from database"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dmaic_projects WHERE id = ?', (self.project_id,))
            row = cursor.fetchone()
            if row:
                self.data = dict(row)
            else:
                self.data = None

    def create_project(self,
                      title: str,
                      problem_statement: str,
                      goal: str,
                      owner: str,
                      target_completion_days: int = 90) -> int:
        """Create new DMAIC project"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO dmaic_projects (
                    title, problem_statement, goal, current_phase,
                    owner, status, target_completion_date, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, datetime('now', ?), CURRENT_TIMESTAMP)
            ''', (
                title,
                problem_statement,
                goal,
                DMAICPhase.DEFINE.value,
                owner,
                'active',
                f'+{target_completion_days} days'
            ))
            self.project_id = cursor.lastrowid

        return self.project_id

    def advance_phase(self, next_phase: DMAICPhase, notes: str):
        """Advance project to next DMAIC phase"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE dmaic_projects
                SET current_phase = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (next_phase.value, self.project_id))

            # Log phase transition
            cursor.execute('''
                INSERT INTO dmaic_phase_logs (
                    project_id, phase, notes, timestamp
                ) VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (self.project_id, next_phase.value, notes))

    def add_measurement(self, metric: str, value: float, notes: Optional[str] = None):
        """Add measurement data point"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO dmaic_measurements (
                    project_id, metric_name, metric_value, notes, measured_at
                ) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (self.project_id, metric, value, notes))

    def complete_project(self, results_summary: str, improvements_achieved: Dict):
        """Complete DMAIC project"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE dmaic_projects
                SET status = 'completed',
                    current_phase = 'control',
                    results_summary = ?,
                    improvements_achieved = ?,
                    completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (results_summary, json.dumps(improvements_achieved), self.project_id))

# ═══════════════════════════════════════════════════════
# QUALITY METRICS TRACKER
# ═══════════════════════════════════════════════════════

def track_system_quality_metrics(days: int = 30) -> Dict:
    """Track overall system quality metrics"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Total operations (logs created)
        cursor.execute('''
            SELECT COUNT(*) as total
            FROM logs
            WHERE timestamp >= datetime('now', ?)
        ''', (f'-{days} days',))
        total_operations = cursor.fetchone()['total']

        # Defects (errors)
        cursor.execute('''
            SELECT COUNT(*) as defects
            FROM system_errors
            WHERE timestamp >= datetime('now', ?)
            AND severity IN ('critical', 'high', 'medium')
        ''', (f'-{days} days',))
        total_defects = cursor.fetchone()['defects']

        # Calculate Sigma level
        sigma_data = sigma_calculator.calculate_sigma_level(total_defects, total_operations)

        # First Pass Yield (operations without errors)
        fpy = ((total_operations - total_defects) / total_operations * 100) if total_operations > 0 else 100

        # Defects by type
        cursor.execute('''
            SELECT component as defect_type, COUNT(*) as count
            FROM system_errors
            WHERE timestamp >= datetime('now', ?)
            GROUP BY component
            ORDER BY count DESC
        ''', (f'-{days} days',))
        defects_by_type = [dict(row) for row in cursor.fetchall()]

        # API response times (for cycle time metric)
        cursor.execute('''
            SELECT AVG(
                CAST((julianday(resolved_at) - julianday(created_at)) * 24 * 60 * 60 AS REAL)
            ) as avg_response_time
            FROM ict_alerts
            WHERE resolved_at IS NOT NULL
            AND created_at >= datetime('now', ?)
        ''', (f'-{days} days',))
        avg_resolution_time = cursor.fetchone()['avg_response_time'] or 0

        return {
            'period_days': days,
            'total_operations': total_operations,
            'total_defects': total_defects,
            'sigma_level': sigma_data['sigma_level'],
            'dpm': sigma_data['dpm'],
            'quality_grade': sigma_data['grade'],
            'first_pass_yield_pct': round(fpy, 2),
            'defects_by_type': defects_by_type,
            'avg_resolution_time_seconds': round(avg_resolution_time, 1),
            'throughput_per_day': round(total_operations / days, 1) if days > 0 else 0
        }

def track_customer_quality_metrics(customer_id: int, days: int = 30) -> Dict:
    """Track quality metrics for specific customer"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Total logs
        cursor.execute('''
            SELECT COUNT(*) as total
            FROM logs
            WHERE customer_id = ?
            AND timestamp >= datetime('now', ?)
        ''', (customer_id, f'-{days} days'))
        total_logs = cursor.fetchone()['total']

        # Errors for this customer
        cursor.execute('''
            SELECT COUNT(*) as defects
            FROM system_errors
            WHERE customer_id = ?
            AND timestamp >= datetime('now', ?)
        ''', (customer_id, f'-{days} days'))
        customer_defects = cursor.fetchone()['defects']

        # Calculate Sigma level for customer
        sigma_data = sigma_calculator.calculate_sigma_level(customer_defects, total_logs)

        # Customer satisfaction proxy (based on activity consistency)
        cursor.execute('''
            SELECT
                COUNT(DISTINCT DATE(timestamp)) as active_days
            FROM logs
            WHERE customer_id = ?
            AND timestamp >= datetime('now', ?)
        ''', (customer_id, f'-{days} days'))
        active_days = cursor.fetchone()['active_days']
        engagement_score = (active_days / days * 100) if days > 0 else 0

        return {
            'customer_id': customer_id,
            'period_days': days,
            'total_operations': total_logs,
            'defects': customer_defects,
            'sigma_level': sigma_data['sigma_level'],
            'dpm': sigma_data['dpm'],
            'quality_grade': sigma_data['grade'],
            'engagement_score': round(engagement_score, 1),
            'active_days': active_days
        }

# ═══════════════════════════════════════════════════════
# PARETO ANALYSIS
# ═══════════════════════════════════════════════════════

def pareto_analysis_defects(days: int = 30) -> Dict:
    """
    Pareto analysis: 80/20 rule for defects
    Identify the 20% of causes that create 80% of problems
    """
    with db.get_db() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                component,
                error_type,
                COUNT(*) as count
            FROM system_errors
            WHERE timestamp >= datetime('now', ?)
            GROUP BY component, error_type
            ORDER BY count DESC
        ''', (f'-{days} days',))

        defects = [dict(row) for row in cursor.fetchall()]

    if not defects:
        return {'defects': [], 'total': 0, 'pareto_80_pct': []}

    total_defects = sum(d['count'] for d in defects)

    # Calculate cumulative percentage
    cumulative = 0
    pareto_80 = []

    for defect in defects:
        cumulative += defect['count']
        cumulative_pct = (cumulative / total_defects * 100)
        defect['cumulative_pct'] = round(cumulative_pct, 1)

        if cumulative_pct <= 80:
            pareto_80.append(defect)

    return {
        'defects': defects,
        'total_defects': total_defects,
        'pareto_80_pct': pareto_80,
        'focus_areas': len(pareto_80),
        'message': f'Focus on fixing {len(pareto_80)} issue types to eliminate 80% of defects'
    }

# ═══════════════════════════════════════════════════════
# CONTINUOUS IMPROVEMENT RECOMMENDATIONS
# ═══════════════════════════════════════════════════════

def get_improvement_recommendations() -> List[Dict]:
    """Generate Lean Six Sigma improvement recommendations"""
    recommendations = []

    # Get current quality metrics
    quality = track_system_quality_metrics(30)

    # Recommendation 1: Sigma level improvement
    if quality['sigma_level'] < 4.0:
        recommendations.append({
            'priority': 'high',
            'category': 'Quality',
            'title': 'Improve Process Quality to 4-Sigma',
            'current_state': f"{quality['sigma_level']}-Sigma ({quality['dpm']} DPM)",
            'target_state': '4-Sigma (6,210 DPM)',
            'action_items': [
                'Implement automated testing to catch defects early',
                'Add input validation on all API endpoints',
                'Create quality gates for deployments'
            ],
            'estimated_impact': 'Reduce defects by 50-70%'
        })

    # Recommendation 2: Pareto analysis
    pareto = pareto_analysis_defects(30)
    if pareto['pareto_80_pct']:
        top_issues = pareto['pareto_80_pct'][:3]
        recommendations.append({
            'priority': 'high',
            'category': 'Defect Reduction',
            'title': 'Focus on Top 3 Defect Causes (80/20 Rule)',
            'current_state': f"{len(top_issues)} issues cause 80% of defects",
            'target_state': 'Eliminate top causes',
            'action_items': [
                f"Fix: {issue['component']} - {issue['error_type']}" for issue in top_issues
            ],
            'estimated_impact': 'Reduce overall defects by 80%'
        })

    # Recommendation 3: Cycle time improvement
    if quality['avg_resolution_time_seconds'] > 3600:  # > 1 hour
        recommendations.append({
            'priority': 'medium',
            'category': 'Cycle Time',
            'title': 'Reduce Mean Time To Resolution (MTTR)',
            'current_state': f"{quality['avg_resolution_time_seconds'] / 60:.0f} minutes",
            'target_state': '< 30 minutes',
            'action_items': [
                'Implement automated incident response playbooks',
                'Create runbooks for common issues',
                'Set up automated alerting'
            ],
            'estimated_impact': 'Reduce downtime by 50%'
        })

    # Recommendation 4: First Pass Yield
    if quality['first_pass_yield_pct'] < 99.0:
        recommendations.append({
            'priority': 'medium',
            'category': 'First Pass Yield',
            'title': 'Improve First-Time-Right Quality',
            'current_state': f"{quality['first_pass_yield_pct']:.1f}% FPY",
            'target_state': '99.0% FPY',
            'action_items': [
                'Add pre-flight checks for data quality',
                'Implement schema validation',
                'Add user input sanitization'
            ],
            'estimated_impact': 'Reduce rework by 30%'
        })

    return recommendations

# ═══════════════════════════════════════════════════════
# DMAIC DASHBOARD
# ═══════════════════════════════════════════════════════

def get_dmaic_dashboard() -> Dict:
    """Get DMAIC projects dashboard"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Active projects
        cursor.execute('''
            SELECT * FROM dmaic_projects
            WHERE status = 'active'
            ORDER BY created_at DESC
        ''')
        active_projects = [dict(row) for row in cursor.fetchall()]

        # Completed projects
        cursor.execute('''
            SELECT * FROM dmaic_projects
            WHERE status = 'completed'
            ORDER BY completed_at DESC
            LIMIT 10
        ''')
        completed_projects = [dict(row) for row in cursor.fetchall()]

        # Projects by phase
        cursor.execute('''
            SELECT current_phase, COUNT(*) as count
            FROM dmaic_projects
            WHERE status = 'active'
            GROUP BY current_phase
        ''')
        by_phase = {row['current_phase']: row['count'] for row in cursor.fetchall()}

    # Quality metrics
    quality = track_system_quality_metrics(30)

    # Improvement recommendations
    recommendations = get_improvement_recommendations()

    return {
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'projects_by_phase': by_phase,
        'current_quality': quality,
        'improvement_recommendations': recommendations,
        'sigma_belt_status': _calculate_sigma_belt(quality['sigma_level'])
    }

def _calculate_sigma_belt(sigma_level: float) -> str:
    """Calculate Six Sigma belt level"""
    if sigma_level >= 6.0:
        return 'Master Black Belt 🥋🥋🥋'
    elif sigma_level >= 5.0:
        return 'Black Belt 🥋🥋'
    elif sigma_level >= 4.0:
        return 'Green Belt 🥋'
    elif sigma_level >= 3.0:
        return 'Yellow Belt 📋'
    else:
        return 'White Belt ⚪'

if __name__ == '__main__':
    print("✓ Lean Six Sigma Module loaded")
    quality = track_system_quality_metrics(30)
    print(f"✓ Current Sigma Level: {quality['sigma_level']}-Sigma")
    print(f"✓ Quality Grade: {quality['quality_grade']}")
    print(f"✓ Belt Status: {_calculate_sigma_belt(quality['sigma_level'])}")
