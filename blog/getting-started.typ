// Blog Post Metadata
// title: Getting Started with This Blog
// date: 2024-07-20
// author: Blog Author
// excerpt: Learn how to set up and use this Typst-powered blog system. This guide covers everything from writing your first post to deploying it with GitHub Actions.

= Getting Started with This Blog

Welcome to this Typst-powered blog! This post will guide you through the basics of using this blogging system.

== What is Typst?

Typst is a new markup-based typesetting system that's designed to be as powerful as LaTeX but much easier to learn and use. Here are some key features:

- *Fast compilation*: Much faster than LaTeX
- *Better error messages*: Clear, helpful error reporting
- *Modern syntax*: Clean, readable markup
- *Great math support*: LaTeX-quality math typesetting

== Writing Your First Post

To create a new blog post, simply create a new `.typ` file in the `blog/` folder. Make sure to include the metadata header at the top:

```
// Blog Post Metadata
// title: Your Post Title
// date: YYYY-MM-DD
// author: Your Name
// excerpt: A brief description of your post...
```

== Math Support

One of the best features of Typst is its excellent math support. You can write inline math like $E = m c^2$ or display equations:

$ integral_0^infinity e^(-x^2) dif x = sqrt(pi)/2 $

Complex expressions are also supported:

$ sum_(k=1)^n k^2 = (n(n+1)(2n+1))/6 $

== Code Blocks

You can include code blocks in various languages:

```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

== Deployment

This blog automatically deploys to GitHub Pages whenever you push changes to the main branch. The build process:

1. Compiles all `.typ` files to HTML
2. Generates the blog index
3. Creates the main index page
4. Deploys everything to GitHub Pages

== Next Steps

- Create your own blog posts in the `blog/` folder
- Customize the templates in the `src/` folder
- Add your own images to the `static/` folder
- Enjoy writing in Typst!

Happy blogging! 🎉 