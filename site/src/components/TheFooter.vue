<template>
    <div id="the-footer">
        <p id="copyright">© Copyright AWE - Accessibility Web Engine 2019</p>
    </div>
</template>

<script>
export default {
    name: 'thefooter',
}
</script>

<style scoped>
#the-footer {
    position: static;
    display: flex;
    background-color: #1A1918;
    height: 64px;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin-top: 64px;
}

#copyright {
    color: white;
    font-size: 12px;
}
</style>
