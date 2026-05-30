# -*- coding: utf-8 -*-
import os
import sys
import json
import socket
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ============= CONFIGURAÇÃO =============
PORT = 8080  # Porta do servidor web
# ========================================

# HTML completo da sua aplicação IPTV
HTML_CODE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<title>Cliente IPTV</title>

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial,sans-serif;
}

body{
    background:#111;
    color:white;
}

header{
    background:#1c1c1c;
    padding:15px;
    text-align:center;
    font-size:22px;
    font-weight:bold;
    border-bottom:1px solid #333;
    position:sticky;
    top:0;
    z-index:100;
}

.container{
    padding:15px;
    max-width:1200px;
    margin:0 auto;
}

.card{
    background:#1b1b1b;
    padding:15px;
    border-radius:12px;
    margin-bottom:15px;
}

input, .search-box input{
    width:100%;
    padding:14px;
    margin-top:10px;
    border:none;
    border-radius:10px;
    background:#2a2a2a;
    color:white;
    font-size:16px;
}

.search-box{
    position:relative;
    margin-bottom:15px;
}

.search-box input{
    padding-right:50px;
    margin-top:0;
}

.search-box button{
    position:absolute;
    right:5px;
    top:5px;
    width:auto;
    padding:9px 15px;
    margin:0;
    background:#0a84ff;
}

.search-results{
    max-height:400px;
    overflow-y:auto;
}

.search-result-item{
    display:flex;
    align-items:center;
    gap:15px;
    padding:10px;
    background:#222;
    border-radius:8px;
    margin-bottom:8px;
    cursor:pointer;
    transition:0.3s;
}

.search-result-item:hover{
    background:#333;
    transform:translateX(5px);
}

.search-result-item img{
    width:60px;
    height:60px;
    object-fit:cover;
    border-radius:8px;
}

.search-result-info{
    flex:1;
}

.search-result-title{
    font-weight:bold;
    margin-bottom:5px;
}

.search-result-type{
    font-size:12px;
    color:#0a84ff;
}

.search-result-category{
    font-size:11px;
    color:#888;
}

.close-search{
    background:#ff3b30;
    padding:8px;
    margin-top:10px;
}

button{
    width:100%;
    padding:14px;
    margin-top:10px;
    border:none;
    border-radius:10px;
    background:#0a84ff;
    color:white;
    font-size:16px;
    cursor:pointer;
}

button:active{
    opacity:0.8;
}

.logout{
    background:#ff3b30;
}

.tabs{
    display:flex;
    gap:10px;
    margin-bottom:15px;
}

.tab{
    flex:1;
    text-align:center;
    padding:12px;
    border-radius:10px;
    background:#222;
    cursor:pointer;
    transition:0.3s;
}

.active{
    background:#0a84ff;
}

.carousel{
    display:flex;
    overflow-x:auto;
    gap:10px;
    padding-bottom:10px;
}

.carousel::-webkit-scrollbar{
    height:5px;
}

.carousel::-webkit-scrollbar-track{
    background:#222;
    border-radius:10px;
}

.carousel::-webkit-scrollbar-thumb{
    background:#0a84ff;
    border-radius:10px;
}

.category{
    min-width:140px;
    background:#222;
    padding:12px;
    border-radius:10px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
}

.category:hover{
    background:#0a84ff;
}

.item{
    min-width:180px;
    background:#222;
    border-radius:12px;
    overflow:hidden;
    cursor:pointer;
    transition:0.3s;
}

.item:hover{
    transform:scale(1.05);
}

.item img{
    width:100%;
    height:250px;
    object-fit:cover;
}

.title{
    padding:10px;
    font-size:14px;
    text-align:center;
}

video{
    width:100%;
    border-radius:12px;
    background:black;
}

.hidden{
    display:none;
}

.loading{
    text-align:center;
    padding:20px;
    color:#0a84ff;
}

.error{
    background:#ff3b30;
    color:white;
    padding:10px;
    border-radius:8px;
    margin:10px 0;
    text-align:center;
}

.season-card{
    background:#222;
    border-radius:12px;
    padding:15px;
    margin-bottom:10px;
    cursor:pointer;
    transition:0.3s;
}

.season-card:hover{
    background:#333;
}

.episode-card{
    background:#222;
    border-radius:12px;
    padding:10px;
    margin-bottom:10px;
    cursor:pointer;
    display:flex;
    gap:15px;
    transition:0.3s;
}

.episode-card:hover{
    background:#333;
}

.episode-card img{
    width:120px;
    height:68px;
    object-fit:cover;
    border-radius:8px;
}

.episode-info{
    flex:1;
}

.episode-title{
    font-weight:bold;
    margin-bottom:5px;
}

.episode-info-text{
    font-size:12px;
    color:#888;
}

.back-button{
    background:#555;
    margin-bottom:10px;
    padding:10px;
    text-align:center;
    border-radius:8px;
    cursor:pointer;
}

.back-button:hover{
    background:#666;
}

.series-info{
    display:flex;
    gap:20px;
    margin-bottom:20px;
    padding:15px;
    background:#222;
    border-radius:12px;
}

.series-info img{
    width:200px;
    height:280px;
    object-fit:cover;
    border-radius:12px;
}

.series-details{
    flex:1;
}

.series-name{
    font-size:24px;
    font-weight:bold;
    margin-bottom:10px;
}

.series-plot{
    color:#aaa;
    line-height:1.5;
}

.breadcrumb{
    margin-bottom:15px;
    padding:10px;
    background:#222;
    border-radius:8px;
    cursor:pointer;
}

.breadcrumb span{
    color:#0a84ff;
}

.search-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:15px;
}

.search-header h3{
    margin:0;
}

.clear-search{
    background:#555;
    width:auto;
    padding:8px 15px;
    margin:0;
}

.results-stats{
    color:#888;
    font-size:12px;
    margin-bottom:10px;
    padding:5px;
}
</style>
</head>

<body>
<header>Cliente IPTV</header>

<div class="container">
<div id="loginPage" class="card">
<h2>Login</h2>
<input type="text" id="host" placeholder="http://site.com:8080">
<input type="text" id="username" placeholder="Usuário">
<input type="password" id="password" placeholder="Senha">
<button onclick="login()">Entrar</button>
</div>

<div id="appPage" class="hidden">
<div class="card">
<div class="tabs">
<div class="tab active" id="tabLive" onclick="changeType('live',this)">Canais</div>
<div class="tab" id="tabMovie" onclick="changeType('movie',this)">Filmes</div>
<div class="tab" id="tabSeries" onclick="changeType('series',this)">Séries</div>
</div>
<button onclick="toggleSearch()">🔍 Buscar Conteúdo</button>
<button onclick="loadAccountInfo()">📊 Informações da Conta</button>
<button class="logout" onclick="logout()">🚪 Sair</button>
</div>

<!-- Search Panel -->
<div id="searchPanel" class="card hidden">
<div class="search-header">
<h3>🔍 Buscar em Tudo</h3>
<button class="clear-search" onclick="toggleSearch()">Fechar</button>
</div>
<div class="search-box">
<input type="text" id="searchInput" placeholder="Digite o nome do canal, filme ou série..." onkeyup="searchAllContent(this.value)">
<button onclick="searchAllContent(document.getElementById('searchInput').value)">Buscar</button>
</div>
<div id="searchResults"></div>
</div>

<div class="card">
<h3>Categorias</h3>
<div id="categories" class="carousel"></div>
</div>

<div class="card">
<h3 id="sectionTitle">Conteúdo</h3>
<div id="content" class="carousel"></div>
</div>

<div class="card" id="seasonsContainer" style="display:none;">
<h3>Temporadas</h3>
<div id="seasonsList"></div>
</div>

<div class="card" id="episodesContainer" style="display:none;">
<h3>Episódios</h3>
<div id="episodesList"></div>
</div>

<div class="card">
<h3 id="playerTitle">Player</h3>
<video id="player" controls playsinline></video>
</div>

<div id="accountInfo" class="card hidden"></div>
</div>
</div>

<script>
let currentType = "live";
let currentCategory = null;
let currentSeries = null;
let currentSeason = null;
let seriesData = null;
let isLoading = false;
let allLiveChannels = [];
let allMovies = [];
let allSeries = [];
let searchPanelOpen = false;

const loginPage = document.getElementById("loginPage");
const appPage = document.getElementById("appPage");
const searchPanel = document.getElementById("searchPanel");

window.onload = () => {
    const saved = localStorage.getItem("xtream_login");
    if(saved){
        const data = JSON.parse(saved);
        document.getElementById("host").value = data.host;
        document.getElementById("username").value = data.username;
        document.getElementById("password").value = data.password;
        startApp();
    }
};

function showLoading(elementId, show){
    const element = document.getElementById(elementId);
    if(show && element){
        element.innerHTML = '<div class="loading">Carregando...</div>';
    } else if(element && element.innerHTML === '<div class="loading">Carregando...</div>'){
        element.innerHTML = '';
    }
}

function showError(message){
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.innerText = message;
    document.querySelector('.container').prepend(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}

function toggleSearch(){
    searchPanelOpen = !searchPanelOpen;
    if(searchPanelOpen){
        searchPanel.classList.remove("hidden");
        document.getElementById("searchInput").focus();
        loadAllContentForSearch();
    } else {
        searchPanel.classList.add("hidden");
        document.getElementById("searchResults").innerHTML = "";
        document.getElementById("searchInput").value = "";
    }
}

async function loadAllContentForSearch(){
    if(allLiveChannels.length === 0 && allMovies.length === 0 && allSeries.length === 0){
        showLoading('searchResults', true);
        try{
            const cfg = getConfig();
            
            const liveData = await api("get_live_streams");
            if(Array.isArray(liveData)) allLiveChannels = liveData;
            
            const moviesData = await api("get_vod_streams");
            if(Array.isArray(moviesData)) allMovies = moviesData;
            
            const seriesData = await api("get_series");
            if(Array.isArray(seriesData)) allSeries = seriesData;
            
        } catch(err){
            console.error("Erro ao carregar dados para busca:", err);
        } finally {
            showLoading('searchResults', false);
        }
    }
}

function searchAllContent(query){
    const resultsDiv = document.getElementById("searchResults");
    
    if(!query || query.trim() === ""){
        resultsDiv.innerHTML = '<div class="error">Digite algo para buscar</div>';
        return;
    }
    
    const searchTerm = query.toLowerCase().trim();
    const results = [];
    
    allLiveChannels.forEach(channel => {
        if(channel.name && channel.name.toLowerCase().includes(searchTerm)){
            results.push({
                type: 'live',
                name: channel.name,
                id: channel.stream_id,
                icon: channel.stream_icon,
                category: 'Canal ao vivo',
                data: channel
            });
        }
    });
    
    allMovies.forEach(movie => {
        if(movie.name && movie.name.toLowerCase().includes(searchTerm)){
            results.push({
                type: 'movie',
                name: movie.name,
                id: movie.stream_id,
                icon: movie.stream_icon,
                category: 'Filme',
                data: movie
            });
        }
    });
    
    allSeries.forEach(serie => {
        if(serie.name && serie.name.toLowerCase().includes(searchTerm)){
            results.push({
                type: 'series',
                name: serie.name,
                id: serie.series_id,
                icon: serie.cover || serie.stream_icon,
                category: 'Série',
                data: serie
            });
        }
    });
    
    if(results.length === 0){
        resultsDiv.innerHTML = '<div class="error">Nenhum resultado encontrado para "' + searchTerm + '"</div>';
        return;
    }
    
    resultsDiv.innerHTML = `
        <div class="results-stats">📺 ${results.length} resultado(s) encontrado(s)</div>
        <div class="search-results"></div>
    `;
    
    const resultsContainer = resultsDiv.querySelector('.search-results');
    
    results.forEach(result => {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'search-result-item';
        
        let typeIcon = "";
        if(result.type === 'live') typeIcon = "📺";
        if(result.type === 'movie') typeIcon = "🎬";
        if(result.type === 'series') typeIcon = "📺";
        
        resultDiv.innerHTML = `
            <img src="${result.icon || ''}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'60\\' height=\\'60\\' viewBox=\\'0 0 24 24\\' fill=\\'%23333\\'%3E%3Cpath d=\\'M18 3v2h-2V3H8v2H6V3H4v18h16V3h-2zM6 19v-5h12v5H6z\\'/%3E%3C/svg%3E'">
            <div class="search-result-info">
                <div class="search-result-title">${typeIcon} ${result.name}</div>
                <div class="search-result-type">${result.category}</div>
            </div>
        `;
        
        resultDiv.onclick = () => {
            toggleSearch();
            if(result.type === 'live'){
                playLiveOrMovie(result.data, 'live');
            } else if(result.type === 'movie'){
                playLiveOrMovie(result.data, 'movie');
            } else if(result.type === 'series'){
                const seriesTab = document.getElementById("tabSeries");
                changeType('series', seriesTab);
                setTimeout(() => {
                    loadSeriesSeasons(result.data, getConfig());
                }, 500);
            }
        };
        
        resultsContainer.appendChild(resultDiv);
    });
}

function playLiveOrMovie(item, type){
    const cfg = getConfig();
    let streamUrl = "";
    
    if(type === 'live'){
        streamUrl = `${cfg.host}/live/${cfg.username}/${cfg.password}/${item.stream_id}.m3u8`;
    } else {
        streamUrl = `${cfg.host}/movie/${cfg.username}/${cfg.password}/${item.stream_id}.${item.container_extension || 'mp4'}`;
    }
    
    playVideo(streamUrl, item.name);
}

function login(){
    const host = document.getElementById("host").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if(!host || !username || !password){
        alert("Preencha todos os campos");
        return;
    }

    testConnection(host, username, password);
}

async function testConnection(host, username, password){
    try{
        const testUrl = `${host}/player_api.php?username=${username}&password=${password}`;
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        
        const response = await fetch(testUrl, {
            signal: controller.signal,
            headers: {'Accept': 'application/json'}
        });
        
        clearTimeout(timeoutId);
        
        if(response.ok){
            localStorage.setItem("xtream_login", JSON.stringify({host, username, password}));
            startApp();
        } else {
            alert(`Erro: Servidor respondeu com status ${response.status}`);
        }
    } catch(err){
        if(err.name === 'AbortError'){
            alert("Timeout: Servidor não respondeu em 10 segundos");
        } else {
            alert(`Erro de conexão: ${err.message}`);
        }
        console.error(err);
    }
}

function logout(){
    localStorage.removeItem("xtream_login");
    location.reload();
}

function getConfig(){
    return JSON.parse(localStorage.getItem("xtream_login"));
}

function startApp(){
    loginPage.classList.add("hidden");
    appPage.classList.remove("hidden");
    resetSeriesView();
    loadCategories();
    allLiveChannels = [];
    allMovies = [];
    allSeries = [];
}

function resetSeriesView(){
    currentSeries = null;
    currentSeason = null;
    seriesData = null;
    document.getElementById("seasonsContainer").style.display = "none";
    document.getElementById("episodesContainer").style.display = "none";
    document.getElementById("sectionTitle").innerHTML = "Conteúdo";
    document.getElementById("sectionTitle").style.cursor = "default";
    document.getElementById("sectionTitle").onclick = null;
}

async function api(action){
    if(isLoading) return [];
    
    isLoading = true;
    
    try{
        const cfg = getConfig();
        let url = `${cfg.host}/player_api.php?username=${cfg.username}&password=${cfg.password}`;
        
        if(action){
            url += `&action=${action}`;
        }
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000);
        
        const response = await fetch(url, {
            signal: controller.signal,
            headers: {'Accept': 'application/json'}
        });
        
        clearTimeout(timeoutId);
        
        if(!response.ok) throw new Error(`HTTP ${response.status}`);
        
        const text = await response.text();
        if(!text || text.trim() === '') return [];
        
        return JSON.parse(text);
        
    } catch(err){
        if(err.name !== 'AbortError'){
            showError(`Erro: ${err.message}`);
        }
        console.error(err);
        return [];
    } finally {
        isLoading = false;
    }
}

async function loadCategories(){
    try{
        showLoading('categories', true);
        resetSeriesView();
        
        let action = "";
        if(currentType === "live") action = "get_live_categories";
        if(currentType === "movie") action = "get_vod_categories";
        if(currentType === "series") action = "get_series_categories";
        
        const data = await api(action);
        const container = document.getElementById("categories");
        container.innerHTML = "";
        
        if(!Array.isArray(data) || data.length === 0){
            container.innerHTML = '<div class="error">Nenhuma categoria encontrada</div>';
            return;
        }
        
        data.forEach(cat => {
            const div = document.createElement("div");
            div.className = "category";
            div.innerText = cat.category_name || cat.name;
            div.onclick = () => {
                currentCategory = cat.category_id;
                resetSeriesView();
                loadContent();
            };
            container.appendChild(div);
        });
        
        if(currentType === "series" && (!currentCategory || data.length === 0)){
            loadContent();
        }
        
    } catch(err){
        console.error("Erro categorias:", err);
        showError("Erro ao carregar categorias");
    } finally {
        showLoading('categories', false);
    }
}

async function loadContent(){
    try{
        showLoading('content', true);
        
        let items = [];
        const cfg = getConfig();
        
        if(currentType === "series"){
            if(currentCategory){
                const action = `get_series&category_id=${currentCategory}`;
                items = await api(action);
            } else {
                items = await api("get_series");
            }
        } 
        else if(currentType === "live" && currentCategory){
            const action = `get_live_streams&category_id=${currentCategory}`;
            items = await api(action);
        }
        else if(currentType === "movie" && currentCategory){
            const action = `get_vod_streams&category_id=${currentCategory}`;
            items = await api(action);
        }
        
        const container = document.getElementById("content");
        container.innerHTML = "";
        
        if(!Array.isArray(items) || items.length === 0){
            container.innerHTML = '<div class="error">Nenhum conteúdo encontrado</div>';
            return;
        }
        
        if(currentType === "series"){
            displaySeriesList(items, cfg);
        } 
        else if(currentType === "live"){
            displayLiveOrMovies(items, cfg, "live");
        }
        else if(currentType === "movie"){
            displayLiveOrMovies(items, cfg, "movie");
        }
        
    } catch(err){
        console.error("Erro conteúdo:", err);
        showError("Erro ao carregar conteúdo");
    } finally {
        showLoading('content', false);
    }
}

function displaySeriesList(series, cfg){
    const container = document.getElementById("content");
    container.innerHTML = "";
    
    series.forEach(serie => {
        const div = document.createElement("div");
        div.className = "item";
        const coverImg = serie.cover || serie.stream_icon || '';
        div.innerHTML = `
            <img src="${coverImg}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'100\\' height=\\'100\\' viewBox=\\'0 0 24 24\\' fill=\\'%23333\\'%3E%3Cpath d=\\'M18 3v2h-2V3H8v2H6V3H4v18h16V3h-2zM6 19v-5h12v5H6z\\'/%3E%3C/svg%3E'">
            <div class="title">${serie.name}</div>
        `;
        div.onclick = () => loadSeriesSeasons(serie, cfg);
        container.appendChild(div);
    });
}

function displayLiveOrMovies(items, cfg, type){
    const container = document.getElementById("content");
    container.innerHTML = "";
    
    items.forEach(item => {
        let streamUrl = "";
        if(type === "live"){
            streamUrl = `${cfg.host}/live/${cfg.username}/${cfg.password}/${item.stream_id}.m3u8`;
        } else {
            streamUrl = `${cfg.host}/movie/${cfg.username}/${cfg.password}/${item.stream_id}.${item.container_extension || 'mp4'}`;
        }
        
        const div = document.createElement("div");
        div.className = "item";
        const imgUrl = item.stream_icon || '';
        div.innerHTML = `
            <img src="${imgUrl}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'100\\' height=\\'100\\' viewBox=\\'0 0 24 24\\' fill=\\'%23333\\'%3E%3Cpath d=\\'M18 3v2h-2V3H8v2H6V3H4v18h16V3h-2zM6 19v-5h12v5H6z\\'/%3E%3C/svg%3E'">
            <div class="title">${item.name}</div>
        `;
        div.onclick = () => playVideo(streamUrl, item.name);
        container.appendChild(div);
    });
}

async function loadSeriesSeasons(serie, cfg){
    try{
        showLoading('seasonsList', true);
        
        currentSeries = serie;
        document.getElementById("seasonsContainer").style.display = "block";
        document.getElementById("episodesContainer").style.display = "none";
        document.getElementById("sectionTitle").innerHTML = `📺 ${serie.name} <span style="font-size:12px;color:#888;">(clique para voltar)</span>`;
        document.getElementById("sectionTitle").style.cursor = "pointer";
        document.getElementById("sectionTitle").onclick = () => {
            resetSeriesView();
            loadContent();
        };
        
        const seriesInfo = await api(`get_series_info&series_id=${serie.series_id}`);
        
        if(seriesInfo && seriesInfo.episodes){
            seriesData = seriesInfo;
            
            const seasonsList = document.getElementById("seasonsList");
            seasonsList.innerHTML = "";
            
            const infoDiv = document.createElement("div");
            infoDiv.className = "series-info";
            infoDiv.innerHTML = `
                <img src="${seriesInfo.info.cover || ''}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'200\\' height=\\'280\\' viewBox=\\'0 0 24 24\\' fill=\\'%23333\\'%3E%3Cpath d=\\'M18 3v2h-2V3H8v2H6V3H4v18h16V3h-2zM6 19v-5h12v5H6z\\'/%3E%3C/svg%3E'">
                <div class="series-details">
                    <div class="series-name">${seriesInfo.info.name}</div>
                    <div class="series-plot">${seriesInfo.info.plot || 'Sem descrição'}</div>
                    <div style="margin-top:10px;">⭐ ${seriesInfo.info.rating || 'N/A'} | 🎬 ${seriesInfo.info.releaseDate || 'Data desconhecida'}</div>
                </div>
            `;
            seasonsList.appendChild(infoDiv);
            
            const seasons = Object.keys(seriesInfo.episodes);
            seasons.forEach(seasonNum => {
                const seasonDiv = document.createElement("div");
                seasonDiv.className = "season-card";
                seasonDiv.innerHTML = `
                    <div style="font-weight:bold;font-size:18px;">Temporada ${seasonNum}</div>
                    <div style="color:#888;">${seriesInfo.episodes[seasonNum].length} episódios</div>
                `;
                seasonDiv.onclick = () => loadEpisodes(seasonNum, seriesInfo.episodes[seasonNum], cfg);
                seasonsList.appendChild(seasonDiv);
            });
        }
        
    } catch(err){
        console.error("Erro ao carregar temporadas:", err);
        showError("Erro ao carregar informações da série");
    } finally {
        showLoading('seasonsList', false);
    }
}

async function loadEpisodes(seasonNum, episodes, cfg){
    try{
        currentSeason = seasonNum;
        
        const breadcrumb = document.createElement("div");
        breadcrumb.className = "breadcrumb";
        breadcrumb.innerHTML = `← Voltar para <span>Temporadas</span>`;
        breadcrumb.onclick = () => {
            document.getElementById("episodesContainer").style.display = "none";
            document.getElementById("seasonsContainer").style.display = "block";
        };
        
        const episodesList = document.getElementById("episodesList");
        episodesList.innerHTML = "";
        episodesList.appendChild(breadcrumb);
        
        episodes.forEach(ep => {
            const epDiv = document.createElement("div");
            epDiv.className = "episode-card";
            
            const streamUrl = `${cfg.host}/series/${cfg.username}/${cfg.password}/${ep.id}.${ep.container_extension || 'mp4'}`;
            
            epDiv.innerHTML = `
                <img src="${ep.info.movie_image || ''}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'120\\' height=\\'68\\' viewBox=\\'0 0 24 24\\' fill=\\'%23333\\'%3E%3Cpath d=\\'M18 3v2h-2V3H8v2H6V3H4v18h16V3h-2zM6 19v-5h12v5H6z\\'/%3E%3C/svg%3E'">
                <div class="episode-info">
                    <div class="episode-title">${ep.episode_num} - ${ep.title}</div>
                    <div class="episode-info-text">${ep.info.duration_s ? Math.floor(ep.info.duration_s / 60) + ' min' : 'Duração desconhecida'}</div>
                    <div class="episode-info-text">${ep.info.plot || ''}</div>
                </div>
            `;
            
            epDiv.onclick = () => playVideo(streamUrl, `${seriesData.info.name} - T${seasonNum}E${ep.episode_num}: ${ep.title}`);
            episodesList.appendChild(epDiv);
        });
        
        document.getElementById("seasonsContainer").style.display = "none";
        document.getElementById("episodesContainer").style.display = "block";
        
    } catch(err){
        console.error("Erro ao carregar episódios:", err);
        showError("Erro ao carregar episódios");
    }
}

function playVideo(url, title){
    try{
        const player = document.getElementById("player");
        player.src = url;
        document.getElementById("playerTitle").innerText = title;
        document.title = title;
        
        player.play().catch(e => {
            showError("Erro ao reproduzir: " + e.message);
        });
        
    } catch(err){
        console.error("Erro player:", err);
        showError("Erro ao iniciar reprodução");
    }
}

async function loadAccountInfo(){
    try{
        const data = await api('');
        
        if(data && data.user_info){
            const info = data.user_info;
            const server = data.server_info;
            
            const box = document.getElementById("accountInfo");
            box.classList.remove("hidden");
            box.innerHTML = `
                <h3>Informações da Conta</h3>
                <p><strong>Status:</strong> ${info.status || 'N/A'}</p>
                <p><strong>Usuários conectados:</strong> ${server?.active_cons || 'N/A'}</p>
                <p><strong>Máximo conexões:</strong> ${info.max_connections || 'N/A'}</p>
                <p><strong>Servidor:</strong> ${server?.url || 'N/A'}</p>
                <p><strong>Expira:</strong> ${info.exp_date ? new Date(info.exp_date * 1000).toLocaleString() : 'N/A'}</p>
            `;
        } else {
            showError("Não foi possível carregar informações da conta");
        }
        
    } catch(err){
        console.error("Erro conta:", err);
        showError("Erro ao carregar informações da conta");
    }
}

function changeType(type, element){
    currentType = type;
    currentCategory = null;
    resetSeriesView();
    
    document.querySelectorAll(".tab").forEach(tab => {
        tab.classList.remove("active");
    });
    element.classList.add("active");
    
    loadCategories();
}
</script>
</body>
</html>'''

class WebHandler(BaseHTTPRequestHandler):
    """Handler para requisições HTTP"""
    
    def do_GET(self):
        """Processa requisições GET"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            # Envia a página HTML
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(HTML_CODE.encode('utf-8'))
            
        elif parsed_path.path == '/status':
            # Endpoint de status
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'running'}).encode())
            
        else:
            # 404 para outros arquivos
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Pagina nao encontrada</h1>')
    
    def log_message(self, format, *args):
        """Override para mostrar mensagens de log formatadas"""
        print(f"[{time.strftime('%H:%M:%S')}] {args[0]}" if args else format)
    
    def do_OPTIONS(self):
        """Responde a requisições OPTIONS (CORS)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def get_local_ip():
    """Obtém o IP local da máquina"""
    try:
        # Cria um socket para obter o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_server():
    """Inicia o servidor HTTP"""
    server = HTTPServer(('0.0.0.0', PORT), WebHandler)
    
    # Obtém IPs disponíveis
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print("🎬 SERVIDOR IPTV INICIADO COM SUCESSO!")
    print("="*60)
    print(f"\n📱 ACESSE NO SEU DISPOSITIVO:")
    print(f"   • Local (mesmo dispositivo): \nhttp://localhost:{PORT}")
    print(f"   • Rede local (outros dispositivos): \nhttp://{local_ip}:{PORT}")
    print(f"\n💡 DICAS:")
    print(f"   • Use o WebVideoCaster para transmitir para TV")
    print(f"   • Certifique-se que os dispositivos estão na mesma rede Wi-Fi")
    print(f"\n⚠️  Para parar o servidor: Pressione Ctrl+C")
    print("="*60 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor encerrado pelo usuário")
        server.shutdown()

if __name__ == '__main__':
    print("\n🚀 Iniciando Servidor Web IPTV...")
    print(f"📡 Porta configurada: {PORT}")
    
    # Inicia servidor
    start_server()
