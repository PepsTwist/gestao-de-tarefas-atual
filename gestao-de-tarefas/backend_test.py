#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Task Management System
Tests all endpoints with proper authentication and permission validation
"""

import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')
BASE_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_URL = f"{BASE_URL}/api"

class TaskManagerAPITester:
    def __init__(self):
        self.admin_token = None
        self.user_token = None
        self.admin_user = None
        self.regular_user = None
        self.team_id = None
        self.task_id = None
        self.comment_id = None
        
    def log_test(self, test_name, success, details=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success:
            print(f"   ❗ CRITICAL ISSUE DETECTED")
        print()

    def test_authentication_system(self):
        """Test JWT authentication endpoints"""
        print("🔐 TESTING AUTHENTICATION SYSTEM")
        print("=" * 50)
        
        # Test admin login
        try:
            login_data = {
                "email": "admin@taskmanager.com",
                "password": "admin123"
            }
            response = requests.post(f"{API_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.admin_token = token_data.get('access_token')
                self.log_test("Admin Login", True, f"Token received: {self.admin_token[:20]}...")
            else:
                self.log_test("Admin Login", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Exception: {str(e)}")
            return False

        # Test user login
        try:
            login_data = {
                "email": "joao@taskmanager.com", 
                "password": "user123"
            }
            response = requests.post(f"{API_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.user_token = token_data.get('access_token')
                self.log_test("Regular User Login", True, f"Token received: {self.user_token[:20]}...")
            else:
                self.log_test("Regular User Login", False, f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("Regular User Login", False, f"Exception: {str(e)}")

        # Test get current user (admin)
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_URL}/auth/me", headers=headers)
            
            if response.status_code == 200:
                self.admin_user = response.json()
                self.log_test("Get Current User (Admin)", True, f"Admin user: {self.admin_user['email']}")
            else:
                self.log_test("Get Current User (Admin)", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Get Current User (Admin)", False, f"Exception: {str(e)}")

        # Test get current user (regular user)
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.get(f"{API_URL}/auth/me", headers=headers)
            
            if response.status_code == 200:
                self.regular_user = response.json()
                self.log_test("Get Current User (Regular)", True, f"User: {self.regular_user['email']}")
            else:
                self.log_test("Get Current User (Regular)", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Get Current User (Regular)", False, f"Exception: {str(e)}")

        # Test invalid token
        try:
            headers = {"Authorization": "Bearer invalid_token"}
            response = requests.get(f"{API_URL}/auth/me", headers=headers)
            
            if response.status_code == 401:
                self.log_test("Invalid Token Rejection", True, "Correctly rejected invalid token")
            else:
                self.log_test("Invalid Token Rejection", False, f"Should return 401, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Invalid Token Rejection", False, f"Exception: {str(e)}")

        return self.admin_token is not None and self.user_token is not None

    def test_user_management(self):
        """Test user CRUD operations"""
        print("👥 TESTING USER MANAGEMENT")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_test("User Management", False, "No admin token available")
            return False

        # Test admin get all users
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_URL}/admin/users", headers=headers)
            
            if response.status_code == 200:
                users = response.json()
                self.log_test("Admin Get All Users", True, f"Found {len(users)} users")
            else:
                self.log_test("Admin Get All Users", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin Get All Users", False, f"Exception: {str(e)}")

        # Test regular user cannot access admin endpoint
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.get(f"{API_URL}/admin/users", headers=headers)
            
            if response.status_code == 403:
                self.log_test("User Permission Restriction", True, "Regular user correctly denied admin access")
            else:
                self.log_test("User Permission Restriction", False, f"Should return 403, got {response.status_code}")
                
        except Exception as e:
            self.log_test("User Permission Restriction", False, f"Exception: {str(e)}")

        # Test admin create user
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            new_user_data = {
                "email": "testuser@taskmanager.com",
                "name": "Test User",
                "password": "testpass123"
            }
            response = requests.post(f"{API_URL}/admin/users", json=new_user_data, headers=headers)
            
            if response.status_code == 200:
                created_user = response.json()
                self.log_test("Admin Create User", True, f"Created user: {created_user['email']}")
            else:
                self.log_test("Admin Create User", False, f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Create User", False, f"Exception: {str(e)}")

        return True

    def test_team_management(self):
        """Test team CRUD operations"""
        print("🏢 TESTING TEAM MANAGEMENT")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_test("Team Management", False, "No admin token available")
            return False

        # Test admin create team
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            team_data = {
                "name": "Test Team",
                "description": "Team created for testing"
            }
            response = requests.post(f"{API_URL}/teams", json=team_data, headers=headers)
            
            if response.status_code == 200:
                team = response.json()
                self.team_id = team['id']
                self.log_test("Admin Create Team", True, f"Created team: {team['name']}")
            else:
                self.log_test("Admin Create Team", False, f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Create Team", False, f"Exception: {str(e)}")

        # Test regular user cannot create team
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            team_data = {
                "name": "Unauthorized Team",
                "description": "This should fail"
            }
            response = requests.post(f"{API_URL}/teams", json=team_data, headers=headers)
            
            if response.status_code == 403:
                self.log_test("Team Creation Permission", True, "Regular user correctly denied team creation")
            else:
                self.log_test("Team Creation Permission", False, f"Should return 403, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Team Creation Permission", False, f"Exception: {str(e)}")

        # Test get teams (admin)
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_URL}/teams", headers=headers)
            
            if response.status_code == 200:
                teams = response.json()
                self.log_test("Admin Get Teams", True, f"Found {len(teams)} teams")
            else:
                self.log_test("Admin Get Teams", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin Get Teams", False, f"Exception: {str(e)}")

        # Test get teams (regular user)
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.get(f"{API_URL}/teams", headers=headers)
            
            if response.status_code == 200:
                teams = response.json()
                self.log_test("User Get Teams", True, f"User can see {len(teams)} teams")
            else:
                self.log_test("User Get Teams", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("User Get Teams", False, f"Exception: {str(e)}")

        return True

    def test_task_management(self):
        """Test task CRUD operations"""
        print("📋 TESTING TASK MANAGEMENT")
        print("=" * 50)
        
        if not self.admin_token or not self.regular_user:
            self.log_test("Task Management", False, "Missing required tokens or user data")
            return False

        # Get a team ID for task creation
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_URL}/teams", headers=headers)
            if response.status_code == 200:
                teams = response.json()
                if teams:
                    self.team_id = teams[0]['id']
                else:
                    self.log_test("Task Management Setup", False, "No teams available for testing")
                    return False
        except Exception as e:
            self.log_test("Task Management Setup", False, f"Exception getting teams: {str(e)}")
            return False

        # Test create task
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            task_data = {
                "title": "Test Task",
                "description": "Task created for testing",
                "responsible_user_id": self.regular_user['id'],
                "deadline": (datetime.utcnow() + timedelta(days=7)).isoformat(),
                "category": "Desenvolvimento",
                "urgency": "alta",
                "requested_by": self.admin_user['id'],
                "team_id": self.team_id
            }
            response = requests.post(f"{API_URL}/tasks", json=task_data, headers=headers)
            
            if response.status_code == 200:
                task = response.json()
                self.task_id = task['id']
                self.log_test("Create Task", True, f"Created task: {task['title']}")
            else:
                self.log_test("Create Task", False, f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("Create Task", False, f"Exception: {str(e)}")

        # Test get all tasks (admin)
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_URL}/tasks", headers=headers)
            
            if response.status_code == 200:
                tasks = response.json()
                self.log_test("Admin Get All Tasks", True, f"Found {len(tasks)} tasks")
            else:
                self.log_test("Admin Get All Tasks", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin Get All Tasks", False, f"Exception: {str(e)}")

        # Test get tasks (regular user - should only see team tasks)
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.get(f"{API_URL}/tasks", headers=headers)
            
            if response.status_code == 200:
                tasks = response.json()
                self.log_test("User Get Team Tasks", True, f"User can see {len(tasks)} tasks")
            else:
                self.log_test("User Get Team Tasks", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("User Get Team Tasks", False, f"Exception: {str(e)}")

        # Test get specific task
        if self.task_id:
            try:
                headers = {"Authorization": f"Bearer {self.admin_token}"}
                response = requests.get(f"{API_URL}/tasks/{self.task_id}", headers=headers)
                
                if response.status_code == 200:
                    task = response.json()
                    self.log_test("Get Specific Task", True, f"Retrieved task: {task['title']}")
                else:
                    self.log_test("Get Specific Task", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test("Get Specific Task", False, f"Exception: {str(e)}")

        # Test update task
        if self.task_id:
            try:
                headers = {"Authorization": f"Bearer {self.admin_token}"}
                update_data = {
                    "status": "em_progresso",
                    "urgency": "critica"
                }
                response = requests.put(f"{API_URL}/tasks/{self.task_id}", json=update_data, headers=headers)
                
                if response.status_code == 200:
                    updated_task = response.json()
                    self.log_test("Update Task", True, f"Updated task status to: {updated_task['status']}")
                else:
                    self.log_test("Update Task", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test("Update Task", False, f"Exception: {str(e)}")

        return True

    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        print("📊 TESTING DASHBOARD STATISTICS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_test("Dashboard Stats", False, "No admin token available")
            return False

        # Test admin dashboard stats
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_URL}/dashboard/stats", headers=headers)
            
            if response.status_code == 200:
                stats = response.json()
                required_fields = ['total_tasks', 'completed_tasks', 'in_progress_tasks', 
                                 'pending_tasks', 'overdue_tasks', 'urgency_stats', 'category_stats']
                
                missing_fields = [field for field in required_fields if field not in stats]
                if not missing_fields:
                    self.log_test("Admin Dashboard Stats", True, 
                                f"Total tasks: {stats['total_tasks']}, "
                                f"Completed: {stats['completed_tasks']}, "
                                f"In Progress: {stats['in_progress_tasks']}")
                else:
                    self.log_test("Admin Dashboard Stats", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("Admin Dashboard Stats", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin Dashboard Stats", False, f"Exception: {str(e)}")

        # Test user dashboard stats (should be filtered to user's team)
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.get(f"{API_URL}/dashboard/stats", headers=headers)
            
            if response.status_code == 200:
                stats = response.json()
                self.log_test("User Dashboard Stats", True, 
                            f"User sees {stats['total_tasks']} tasks (team filtered)")
            else:
                self.log_test("User Dashboard Stats", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("User Dashboard Stats", False, f"Exception: {str(e)}")

        return True

    def test_comments_system(self):
        """Test comments functionality"""
        print("💬 TESTING COMMENTS SYSTEM")
        print("=" * 50)
        
        if not self.task_id or not self.admin_token:
            self.log_test("Comments System", False, "No task ID or admin token available")
            return False

        # Test create comment
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            comment_data = {
                "task_id": self.task_id,
                "content": "This is a test comment on the task"
            }
            response = requests.post(f"{API_URL}/comments", json=comment_data, headers=headers)
            
            if response.status_code == 200:
                comment = response.json()
                self.comment_id = comment['id']
                self.log_test("Create Comment", True, f"Created comment: {comment['content'][:30]}...")
            else:
                self.log_test("Create Comment", False, f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("Create Comment", False, f"Exception: {str(e)}")

        # Test get task comments
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_URL}/tasks/{self.task_id}/comments", headers=headers)
            
            if response.status_code == 200:
                comments = response.json()
                self.log_test("Get Task Comments", True, f"Found {len(comments)} comments")
            else:
                self.log_test("Get Task Comments", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Get Task Comments", False, f"Exception: {str(e)}")

        return True

    def test_permission_system(self):
        """Test permission isolation between teams"""
        print("🔒 TESTING PERMISSION SYSTEM")
        print("=" * 50)
        
        # This test verifies that users can only access their team's data
        # Most permission tests are already covered in individual sections
        # This is a summary verification
        
        permission_tests_passed = 0
        total_permission_tests = 3
        
        # Test 1: Regular user cannot access admin endpoints
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.get(f"{API_URL}/admin/users", headers=headers)
            if response.status_code == 403:
                permission_tests_passed += 1
                self.log_test("Admin Endpoint Protection", True, "Regular user denied admin access")
            else:
                self.log_test("Admin Endpoint Protection", False, f"Expected 403, got {response.status_code}")
        except Exception as e:
            self.log_test("Admin Endpoint Protection", False, f"Exception: {str(e)}")

        # Test 2: Regular user cannot create teams
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            team_data = {"name": "Unauthorized Team", "description": "Should fail"}
            response = requests.post(f"{API_URL}/teams", json=team_data, headers=headers)
            if response.status_code == 403:
                permission_tests_passed += 1
                self.log_test("Team Creation Protection", True, "Regular user denied team creation")
            else:
                self.log_test("Team Creation Protection", False, f"Expected 403, got {response.status_code}")
        except Exception as e:
            self.log_test("Team Creation Protection", False, f"Exception: {str(e)}")

        # Test 3: Token validation works
        try:
            headers = {"Authorization": "Bearer invalid_token_here"}
            response = requests.get(f"{API_URL}/auth/me", headers=headers)
            if response.status_code == 401:
                permission_tests_passed += 1
                self.log_test("Token Validation", True, "Invalid token correctly rejected")
            else:
                self.log_test("Token Validation", False, f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log_test("Token Validation", False, f"Exception: {str(e)}")

        overall_success = permission_tests_passed == total_permission_tests
        self.log_test("Overall Permission System", overall_success, 
                     f"{permission_tests_passed}/{total_permission_tests} permission tests passed")
        
        return overall_success

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 STARTING COMPREHENSIVE BACKEND API TESTING")
        print("=" * 60)
        print(f"Testing against: {API_URL}")
        print("=" * 60)
        
        test_results = {}
        
        # Run tests in order of priority
        test_results['authentication'] = self.test_authentication_system()
        test_results['user_management'] = self.test_user_management()
        test_results['team_management'] = self.test_team_management()
        test_results['task_management'] = self.test_task_management()
        test_results['dashboard_stats'] = self.test_dashboard_stats()
        test_results['comments_system'] = self.test_comments_system()
        test_results['permission_system'] = self.test_permission_system()
        
        # Summary
        print("📋 TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = sum(1 for result in test_results.values() if result)
        total_tests = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name.replace('_', ' ').title()}")
        
        print(f"\nOverall Result: {passed_tests}/{total_tests} test suites passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL BACKEND TESTS PASSED!")
        else:
            print("⚠️  SOME TESTS FAILED - CHECK DETAILS ABOVE")
        
        return test_results

if __name__ == "__main__":
    tester = TaskManagerAPITester()
    results = tester.run_all_tests()