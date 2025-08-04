import React, { useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Task Manager Component
const TaskManager = ({ tasks, onTasksChange, getUrgencyColor, getStatusColor }) => {
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    responsible_user_id: "",
    deadline: "",
    category: "",
    urgency: "media",
    team_id: "",
    requested_by: ""
  });

  useEffect(() => {
    fetchUsers();
    fetchTeams();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API}/users`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchTeams = async () => {
    try {
      const response = await axios.get(`${API}/teams`);
      setTeams(response.data);
    } catch (error) {
      console.error('Error fetching teams:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingTask) {
        await axios.put(`${API}/tasks/${editingTask.id}`, formData);
      } else {
        await axios.post(`${API}/tasks`, formData);
      }
      setShowModal(false);
      setEditingTask(null);
      resetForm();
      onTasksChange();
    } catch (error) {
      console.error('Error saving task:', error);
      alert('Erro ao salvar tarefa');
    }
  };

  const handleEdit = (task) => {
    setEditingTask(task);
    setFormData({
      title: task.title,
      description: task.description || "",
      responsible_user_id: task.responsible_user_id,
      deadline: task.deadline ? task.deadline.split('T')[0] : "",
      category: task.category,
      urgency: task.urgency,
      team_id: task.team_id,
      requested_by: task.requested_by
    });
    setShowModal(true);
  };

  const handleDelete = async (taskId) => {
    if (window.confirm('Tem certeza que deseja excluir esta tarefa?')) {
      try {
        await axios.delete(`${API}/tasks/${taskId}`);
        onTasksChange();
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Erro ao excluir tarefa');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      title: "",
      description: "",
      responsible_user_id: "",
      deadline: "",
      category: "",
      urgency: "media",
      team_id: "",
      requested_by: ""
    });
  };

  const getUserName = (userId) => {
    const user = users.find(u => u.id === userId);
    return user ? user.name : 'Usuário não encontrado';
  };

  const getTeamName = (teamId) => {
    const team = teams.find(t => t.id === teamId);
    return team ? team.name : 'Equipe não encontrada';
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-900">Gerenciar Tarefas</h2>
        <button
          onClick={() => {
            resetForm();
            setEditingTask(null);
            setShowModal(true);
          }}
          className="btn-primary"
        >
          <svg className="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Nova Tarefa
        </button>
      </div>

      {/* Tasks Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tasks.map((task) => (
          <div key={task.id} className="task-card">
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">{task.title}</h3>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleEdit(task)}
                  className="text-purple-600 hover:text-purple-800 p-1"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  onClick={() => handleDelete(task.id)}
                  className="text-red-600 hover:text-red-800 p-1"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
            
            <p className="text-gray-600 text-sm mb-3 line-clamp-2">
              {task.description || "Sem descrição"}
            </p>
            
            <div className="space-y-2 mb-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Responsável:</span>
                <span className="text-gray-900 font-medium">{getUserName(task.responsible_user_id)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Equipe:</span>
                <span className="text-gray-900">{getTeamName(task.team_id)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Categoria:</span>
                <span className="text-gray-900">{task.category}</span>
              </div>
              {task.deadline && (
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Prazo:</span>
                  <span className="text-gray-900">{new Date(task.deadline).toLocaleDateString('pt-BR')}</span>
                </div>
              )}
            </div>
            
            <div className="flex justify-between items-center">
              <div className="flex space-x-2">
                <span className={`badge badge-urgency-${task.urgency}`}>
                  {task.urgency}
                </span>
                <span className={`badge badge-status-${task.status}`}>
                  {task.status.replace('_', ' ')}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900">
                  {editingTask ? 'Editar Tarefa' : 'Nova Tarefa'}
                </h3>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Título *</label>
                  <input
                    type="text"
                    required
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    className="form-input"
                    placeholder="Título da tarefa"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    className="form-textarea"
                    rows="3"
                    placeholder="Descrição detalhada da tarefa"
                  />
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Responsável *</label>
                    <select
                      required
                      value={formData.responsible_user_id}
                      onChange={(e) => setFormData({...formData, responsible_user_id: e.target.value})}
                      className="form-select"
                    >
                      <option value="">Selecione um responsável</option>
                      {users.map((user) => (
                        <option key={user.id} value={user.id}>{user.name}</option>
                      ))}
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Equipe *</label>
                    <select
                      required
                      value={formData.team_id}
                      onChange={(e) => setFormData({...formData, team_id: e.target.value})}
                      className="form-select"
                    >
                      <option value="">Selecione uma equipe</option>
                      {teams.map((team) => (
                        <option key={team.id} value={team.id}>{team.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Categoria *</label>
                    <input
                      type="text"
                      required
                      value={formData.category}
                      onChange={(e) => setFormData({...formData, category: e.target.value})}
                      className="form-input"
                      placeholder="Ex: Desenvolvimento, Marketing, etc."
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Urgência *</label>
                    <select
                      required
                      value={formData.urgency}
                      onChange={(e) => setFormData({...formData, urgency: e.target.value})}
                      className="form-select"
                    >
                      <option value="baixa">Baixa</option>
                      <option value="media">Média</option>
                      <option value="alta">Alta</option>
                      <option value="critica">Crítica</option>
                    </select>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Prazo</label>
                    <input
                      type="date"
                      value={formData.deadline}
                      onChange={(e) => setFormData({...formData, deadline: e.target.value})}
                      className="form-input"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Solicitado por *</label>
                    <select
                      required
                      value={formData.requested_by}
                      onChange={(e) => setFormData({...formData, requested_by: e.target.value})}
                      className="form-select"
                    >
                      <option value="">Quem solicitou</option>
                      {users.map((user) => (
                        <option key={user.id} value={user.id}>{user.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
                
                {editingTask && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                    <select
                      value={formData.status || editingTask.status}
                      onChange={(e) => setFormData({...formData, status: e.target.value})}
                      className="form-select"
                    >
                      <option value="pendente">Pendente</option>
                      <option value="em_progresso">Em Progresso</option>
                      <option value="concluida">Concluída</option>
                    </select>
                  </div>
                )}
                
                <div className="flex justify-end space-x-4 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="btn-secondary"
                  >
                    Cancelar
                  </button>
                  <button type="submit" className="btn-primary">
                    {editingTask ? 'Atualizar' : 'Criar'} Tarefa
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Kanban Board Component
const KanbanBoard = ({ tasks, onTasksChange, getUrgencyColor, getStatusColor }) => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API}/users`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const getUserName = (userId) => {
    const user = users.find(u => u.id === userId);
    return user ? user.name : 'Usuário não encontrado';
  };

  const updateTaskStatus = async (taskId, newStatus) => {
    try {
      await axios.put(`${API}/tasks/${taskId}`, { status: newStatus });
      onTasksChange();
    } catch (error) {
      console.error('Error updating task status:', error);
      alert('Erro ao atualizar status da tarefa');
    }
  };

  const handleDragStart = (e, taskId) => {
    e.dataTransfer.setData("text/plain", taskId);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e, newStatus) => {
    e.preventDefault();
    const taskId = e.dataTransfer.getData("text/plain");
    updateTaskStatus(taskId, newStatus);
  };

  const columns = [
    { id: 'pendente', title: 'Pendente', color: 'border-yellow-200 bg-yellow-50' },
    { id: 'em_progresso', title: 'Em Progresso', color: 'border-blue-200 bg-blue-50' },
    { id: 'concluida', title: 'Concluída', color: 'border-green-200 bg-green-50' }
  ];

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold text-gray-900">Kanban Board</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {columns.map((column) => (
          <div
            key={column.id}
            className={`kanban-column border-2 ${column.color}`}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, column.id)}
          >
            <div className="kanban-header">
              <h3>{column.title}</h3>
              <span className="text-sm text-gray-500">
                ({tasks.filter(task => task.status === column.id).length})
              </span>
            </div>
            
            <div className="space-y-3">
              {tasks
                .filter(task => task.status === column.id)
                .map((task) => (
                  <div
                    key={task.id}
                    className="kanban-task"
                    draggable
                    onDragStart={(e) => handleDragStart(e, task.id)}
                  >
                    <h4 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                      {task.title}
                    </h4>
                    
                    <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                      {task.description || "Sem descrição"}
                    </p>
                    
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-xs text-gray-500">Responsável:</span>
                      <span className="text-xs text-gray-900 font-medium">
                        {getUserName(task.responsible_user_id)}
                      </span>
                    </div>
                    
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-xs text-gray-500">Categoria:</span>
                      <span className="text-xs text-gray-900">{task.category}</span>
                    </div>
                    
                    {task.deadline && (
                      <div className="flex justify-between items-center mb-3">
                        <span className="text-xs text-gray-500">Prazo:</span>
                        <span className="text-xs text-gray-900">
                          {new Date(task.deadline).toLocaleDateString('pt-BR')}
                        </span>
                      </div>
                    )}
                    
                    <div className="flex justify-center">
                      <span className={`badge badge-urgency-${task.urgency} text-xs`}>
                        {task.urgency}
                      </span>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Admin Panel Component
const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [showUserModal, setShowUserModal] = useState(false);
  const [showTeamModal, setShowTeamModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [userFormData, setUserFormData] = useState({
    email: "",
    name: "",
    password: "",
    team_id: ""
  });
  const [teamFormData, setTeamFormData] = useState({
    name: "",
    description: ""
  });

  useEffect(() => {
    fetchUsers();
    fetchTeams();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API}/admin/users`);
      setUsers(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching users:', error);
      setLoading(false);
    }
  };

  const fetchTeams = async () => {
    try {
      const response = await axios.get(`${API}/teams`);
      setTeams(response.data);
    } catch (error) {
      console.error('Error fetching teams:', error);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/admin/users`, userFormData);
      setShowUserModal(false);
      resetUserForm();
      fetchUsers();
      alert('Usuário criado com sucesso!');
    } catch (error) {
      console.error('Error creating user:', error);
      alert('Erro ao criar usuário: ' + (error.response?.data?.detail || 'Erro desconhecido'));
    }
  };

  const handleCreateTeam = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/teams`, teamFormData);
      setShowTeamModal(false);
      resetTeamForm();
      fetchTeams();
      alert('Equipe criada com sucesso!');
    } catch (error) {
      console.error('Error creating team:', error);
      alert('Erro ao criar equipe: ' + (error.response?.data?.detail || 'Erro desconhecido'));
    }
  };

  const resetUserForm = () => {
    setUserFormData({
      email: "",
      name: "",
      password: "",
      team_id: ""
    });
  };

  const resetTeamForm = () => {
    setTeamFormData({
      name: "",
      description: ""
    });
  };

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
        <p className="text-gray-600">Carregando...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold text-gray-900">Painel Administrativo</h2>
      
      {/* Action Buttons */}
      <div className="flex space-x-4">
        <button
          onClick={() => {
            resetUserForm();
            setShowUserModal(true);
          }}
          className="btn-primary"
        >
          <svg className="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Novo Usuário
        </button>
        
        <button
          onClick={() => {
            resetTeamForm();
            setShowTeamModal(true);
          }}
          className="btn-secondary"
        >
          <svg className="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Nova Equipe
        </button>
      </div>

      {/* Users Table */}
      <div className="bg-white rounded-2xl shadow-sm p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Usuários ({users.length})</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Equipe</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Criado em</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.map((user) => (
                <tr key={user.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{user.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{user.email}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      user.is_admin ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {user.is_admin ? 'Admin' : 'Usuário'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {teams.find(t => t.id === user.team_id)?.name || 'Sem equipe'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(user.created_at).toLocaleDateString('pt-BR')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Teams Table */}
      <div className="bg-white rounded-2xl shadow-sm p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Equipes ({teams.length})</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descrição</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Membros</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Criado em</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {teams.map((team) => (
                <tr key={team.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{team.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{team.description || 'Sem descrição'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {users.filter(u => u.team_id === team.id).length}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(team.created_at).toLocaleDateString('pt-BR')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* User Modal */}
      {showUserModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900">Novo Usuário</h3>
                <button
                  onClick={() => setShowUserModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <form onSubmit={handleCreateUser} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Nome *</label>
                  <input
                    type="text"
                    required
                    value={userFormData.name}
                    onChange={(e) => setUserFormData({...userFormData, name: e.target.value})}
                    className="form-input"
                    placeholder="Nome completo"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Email *</label>
                  <input
                    type="email"
                    required
                    value={userFormData.email}
                    onChange={(e) => setUserFormData({...userFormData, email: e.target.value})}
                    className="form-input"
                    placeholder="email@exemplo.com"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Senha *</label>
                  <input
                    type="password"
                    required
                    value={userFormData.password}
                    onChange={(e) => setUserFormData({...userFormData, password: e.target.value})}
                    className="form-input"
                    placeholder="Senha do usuário"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Equipe</label>
                  <select
                    value={userFormData.team_id}
                    onChange={(e) => setUserFormData({...userFormData, team_id: e.target.value})}
                    className="form-select"
                  >
                    <option value="">Selecione uma equipe</option>
                    {teams.map((team) => (
                      <option key={team.id} value={team.id}>{team.name}</option>
                    ))}
                  </select>
                </div>
                
                <div className="flex justify-end space-x-4 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowUserModal(false)}
                    className="btn-secondary"
                  >
                    Cancelar
                  </button>
                  <button type="submit" className="btn-primary">
                    Criar Usuário
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Team Modal */}
      {showTeamModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900">Nova Equipe</h3>
                <button
                  onClick={() => setShowTeamModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <form onSubmit={handleCreateTeam} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Nome *</label>
                  <input
                    type="text"
                    required
                    value={teamFormData.name}
                    onChange={(e) => setTeamFormData({...teamFormData, name: e.target.value})}
                    className="form-input"
                    placeholder="Nome da equipe"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
                  <textarea
                    value={teamFormData.description}
                    onChange={(e) => setTeamFormData({...teamFormData, description: e.target.value})}
                    className="form-textarea"
                    rows="3"
                    placeholder="Descrição da equipe"
                  />
                </div>
                
                <div className="flex justify-end space-x-4 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowTeamModal(false)}
                    className="btn-secondary"
                  >
                    Cancelar
                  </button>
                  <button type="submit" className="btn-primary">
                    Criar Equipe
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const Components = {
  TaskManager,
  KanbanBoard,
  AdminPanel
};

export default Components;