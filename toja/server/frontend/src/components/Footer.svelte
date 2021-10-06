<script lang="ts">
    import { Link } from 'svelte-navigator';
</script>

<footer class="text-sm mx-auto lg:max-w-screen-md">
    <div role="presentation" class="mb-2">
        <img src="/app/img/element-hr.svg" alt="" class="w-full"/>
    </div>
    <div class="flex flex-row flex-wrap mx-6">
        <nav class="flex-none w-full md:w-3/4 lg:w-1/2 mb-4">
            <ul class="flex flex-row flex-wrap">
                <li role="presentation" class="flex-none w-1/2"><Link to="/about/copyright" class="text-accent">Copyright questions</Link></li>
                <li role="presentation" class="flex-none w-1/2"><Link to="/about/press" class="text-accent">Press &amp; media</Link></li>
                <li role="presentation" class="flex-none w-1/2"><Link to="/about/privacy" class="text-accent">Privacy policy</Link></li>
                <li role="presentation" class="flex-none w-1/2"><Link to="/about/terms" class="text-accent">Terms &amp; Conditions</Link></li>
            </ul>
        </nav>
        <nav class="flex-none w-full md:w-1/4 lg:w-1/2">
            <ul class="flex flex-row justify-end">
                <li role="presentation" class="mr-2">
                    <a href="https://www.facebook.com/VictorianHumour" aria-label="Visit us on Facebook" class="text-accent hover:text-primary transition-colors">
                        <svg viewBox="0 0 51 51" class="w-12 h-12">
                            <path fill="currentColor" d="M32.4895833,23.9583333 L28.125,23.9583333 L28.125,38.5416667 L21.875,38.5416667 L21.875,23.9583333 L17.7083333,23.9583333 L17.7083333,19.7916667 L21.875,19.7916667 L21.875,17.3666667 C21.875,15.0770833 22.6083333,11.4958333 27.3958333,11.4958333 L32.2916667,11.5083333 L32.2916667,16.3125 L29.3583333,16.3125 C28.85,16.3125 28.125,16.5708333 28.125,17.6604167 L28.125,19.7916667 L32.9979167,19.7916667 L32.4895833,23.9583333 Z M25,0 C11.2145833,0 0,11.2145833 0,25 C0,38.7854167 11.2145833,50 25,50 C38.7854167,50 50,38.7854167 50,25 C50,11.2145833 38.7854167,0 25,0 L25,0 Z" />
                        </svg>
                    </a>
                </li>
                <li role="presentation">
                    <a href="https://twitter.com/VictorianHumour" aria-label="Follow us on Twitter" class="text-accent hover:text-primary transition-colors">
                        <svg viewBox="0 0 49 49" class="w-12 h-12">
                            <path fill="currentColor" d="M34.524,18.77 C34.536,18.996 34.54,19.222 34.54,19.45 C34.54,26.406 29.244,34.43 19.562,34.43 C16.59,34.43 13.822,33.556 11.492,32.062 C14.24,32.384 17.036,31.648 19.286,29.884 C16.982,29.84 15.04,28.318 14.37,26.226 C15.162,26.376 15.976,26.348 16.746,26.136 C14.338,25.654 12.524,23.526 12.524,20.978 L12.524,20.908 C13.234,21.302 14.048,21.538 14.908,21.566 C13.496,20.622 12.566,19.012 12.566,17.186 C12.566,16.222 12.826,15.318 13.28,14.538 C15.876,17.724 19.754,19.822 24.13,20.038 C24.04,19.654 23.992,19.25 23.992,18.84 C23.992,15.932 26.35,13.574 29.258,13.574 C30.772,13.574 32.14,14.214 33.1,15.238 C34.3,15 37,14.708 37,14.708 C36.296,15.764 35.554,18.026 34.524,18.77 M24,0 C10.766,0 0,10.766 0,24 C0,37.234 10.766,48 24,48 C37.234,48 48,37.234 48,24 C48,10.766 37.234,0 24,0" />
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>
    </div>
</footer>
