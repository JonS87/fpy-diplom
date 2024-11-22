import { registerUser, loginUser, fetchFiles, uploadFile, deleteFile, fetchUsers, fetchUserData, updateComment, updateFileName } from '../api';

export const setUser = (user) => ({
    type: 'SET_USER',
    payload: user,
});

export const setFiles = (files) => ({
    type: 'SET_FILES',
    payload: files,
});

export const addFile = (file) => ({
    type: 'ADD_FILE',
    payload: file,
});

export const removeFile = (fileId) => ({
    type: 'REMOVE_FILE',
    payload: fileId,
});

export const setUsers = (users) => ({
    type: 'SET_USERS',
    payload: users,
});

export const updateCommentSuccess = (file) => ({
    type: 'UPDATE_COMMENT_SUCCESS',
    payload: { file },
});
export const updateCommentFailure = (error) => ({
    type: 'UPDATE_COMMENT_FAILURE',
    payload: { error },
});

export const updateFileNameSuccess = (file) => ({
    type: 'UPDATE_FILE_NAME_SUCCESS',
    payload: { file },
});

export const updateFileNameFailure = (error) => ({
    type: 'UPDATE_FILE_NAME_FAILURE',
    payload: { error },
});

export const register = (userData) => async (dispatch) => {
    try {
        const response = await registerUser(userData);
        localStorage.setItem('token', response.data.token);
        dispatch(setUser(response.data));
    } catch (error) {
        console.error("Registration failed:", error);
        throw "Registration failed: " + error;
    }
};

export const login = (credentials) => async (dispatch) => {
    try {
        const response = await loginUser(credentials);
        const token = response.data.token;
        localStorage.setItem('token', token);
        dispatch(setUser(response.data));
    } catch (error) {
        console.error("Login failed:", error);
        throw "Login failed: " + error
    }
};

export const logout = () => async (dispatch) => {
        localStorage.removeItem('token');
        dispatch(setUser(null));
};

export const loadFiles = (token) => async (dispatch) => {
    const response = await fetchFiles(token);
    dispatch(setFiles(response.data));
};

export const upload = (file, comment, token) => async (dispatch) => {
    try {
        const response = await uploadFile(file, comment, token);
        dispatch(addFile(response.data));
        dispatch({ type: 'UPLOAD_FILE_SUCCESS', payload: response.data });
    } catch (error) {
        console.error("Ошибка загрузки файла:", error);
        console.log(error.response.data);
        dispatch({ type: 'UPLOAD_FILE_FAILURE', payload: error });
        throw new Error(error.response.data.detail || "Ошибка загрузки файла");
    }
};

export const updateCommentAction = (fileId, comment, token) => async (dispatch) => {
    try {
        const response = await updateComment(fileId, comment, token);
        dispatch(updateCommentSuccess(response.data));
    } catch (error) {
        console.error("Ошибка обновления комментария:", error);
        dispatch(updateCommentFailure(error.response ? error.response.data : error.message));
        throw new Error(error.response.data.detail || "Ошибка обновления комментария");
    }
};

export const updateFileNameAction = (fileId, newName, token) => async (dispatch) => {
    try {
        const response = await updateFileName(fileId, newName, token);
        dispatch(updateFileNameSuccess(response.data));
    } catch (error) {
        console.error("Ошибка обновления имени файла:", error);
        dispatch(updateFileNameFailure(error.response ? error.response.data : error.message));
        throw new Error(error.response.data.detail || "Ошибка обновления имени файла");
    }
};

export const deleteFileAction = (fileId, token) => async (dispatch) => {
    await deleteFile(fileId, token);
    dispatch(removeFile(fileId));
};

export const loadUsers = (token) => async (dispatch) => {
    try {
        const response = await fetchUsers(token);
        dispatch(setUsers(response.data));
    } catch (error) {
        if (error.response && error.response.status === 403) {
            console.error("Доступ запрещен: вы не являетесь администратором.");
        } else {
            console.error("Ошибка при загрузке пользователей:", error);
        }
    }
};

export const checkAuth = () => async (dispatch) => {
    const token = localStorage.getItem('token');
    console.log("Token:", token);
    if (token) {
        try {
            const userResponse = await fetchUserData(token);
            console.log("User Data:", userResponse.data);
            dispatch(setUser(userResponse.data));
        } catch (error) {
            console.error("Failed to fetch user data:", error);
            dispatch(setUser(null));
        }
    } else {
        dispatch(setUser(null));
    }
};
