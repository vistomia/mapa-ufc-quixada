<template>
    <div class="search">
        <div class="container">
            <button>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" style="width: 1em; height: 1em;"><path fill="black" d="M480 272C480 317.9 465.1 360.3 440 394.7L566.6 521.4C579.1 533.9 579.1 554.2 566.6 566.7C554.1 579.2 533.8 579.2 521.3 566.7L394.7 440C360.3 465.1 317.9 480 272 480C157.1 480 64 386.9 64 272C64 157.1 157.1 64 272 64C386.9 64 480 157.1 480 272zM272 416C351.5 416 416 351.5 416 272C416 192.5 351.5 128 272 128C192.5 128 128 192.5 128 272C128 351.5 192.5 416 272 416z"/></svg>
            </button>
            <input type="text" placeholder="Pesquise no MapaUFC" />    
        </div>
    </div>
</template>

<style>
.container {
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2),0 -1px 0px rgba(0,0,0,0.02);
    border-radius: 100px;
    display: flex;
    align-items: center;
    max-width: 400px;
}

.search {
    position: inherit;
    padding: auto;
    width: fit-content;
    z-index: 3;
    display: flex;
    justify-content: center;
    margin-top: 1em;
    margin-left: 4em;
}

.search input {
    padding: 12px 20px;
    border: none;
    outline: none;
    border-radius: 20px 0 0 20px;
    width: 100%;
    font-size: 16px;
    background-color: transparent;
}

.search button {
    padding: 12px 20px;
    border: none;
    color: black;
    background-color: transparent;
    border-radius: 0 20px 20px 0;
    cursor: pointer;
    font-size: 16px;
}
</style>