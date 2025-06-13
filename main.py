#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """
A comprehensive enterprise banking system for financial institutions like American Express.
The system should allow customers to create accounts with KYC validation and multi-currency support.
The system should handle deposits, withdrawals, transfers with real-time fraud detection and AML monitoring.
The system should manage credit card accounts with spending limits, rewards tracking, and merchant payments.
The system should process loans with risk assessment, credit scoring, and automated approval workflows.
The system should maintain regulatory compliance with PCI DSS, BSA, and CFPB reporting requirements.
The system should provide real-time dashboards, transaction analytics, and customer lifetime value calculations.
The system should implement ACID transactions, audit trails, and role-based access control for security.
The system should prevent overdrafts, detect suspicious activities, and maintain encrypted data storage.
The system has access to external APIs for credit scores, exchange rates, and regulatory reporting feeds.

"""
module_name = "banking_core.py"
class_name = "EnterpriseBankingSystem"

def run():
    """Run the banking crew."""

    inputs = {
        'requirements': requirements,
        'module_name' : module_name,
        'class_name' : class_name,
    }

    # create and run the crew
    result = EngineeringTeam().crew().kickoff(inputs= inputs)

if __name__ == "__main__":
    run()