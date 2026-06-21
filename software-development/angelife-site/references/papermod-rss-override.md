# PaperMod rss.xml Override — Hugo 0.124+ Compatibility

## The Problem

Hugo 0.124+ changed `site.Author` from `map[string]interface{}` to untyped `interface{}`.
PaperMod's `themes/PaperMod/layouts/_default/rss.xml` does:

```go
{{- with site.Author.email }}
  {{- $authorEmail = . }}
{{- end }}
```

This throws: `can't evaluate field Author in type interface {}`

## The Fix

Override PaperMod's template at the site level:

```
hugo-site/layouts/_default/rss.xml
```

**Important:** Do NOT add a `site.Author` fallback block. Even `{{- with site.Author }}` throws `can't evaluate field Author in type interface {}` in Hugo 0.162. The entire expression `site.Author` now returns `interface{}` and cannot be evaluated. **Only use `site.Params.author`** — it works correctly.

## Complete Working Template

Copy this file to `hugo-site/layouts/_default/rss.xml`. This is the only correct version — the `site.Author` fallback is absent:

```xml
{{- $authorEmail := "" }}
{{- with site.Params.author }}
  {{- if reflect.IsMap . }}
    {{- with .email }}
      {{- $authorEmail = . }}
    {{- end }}
  {{- end }}
{{- end }}

{{- $authorName := "" }}
{{- with site.Params.author }}
  {{- if reflect.IsMap . }}
    {{- with .name }}
      {{- $authorName = . }}
    {{- end }}
  {{- else }}
    {{- $authorName = . }}
  {{- end }}
{{- end }}

{{- $pctx := . }}
{{- if .IsHome }}{{ $pctx = site }}{{ end }}
{{- $pages := slice }}
{{- if or $.IsHome $.IsSection }}
{{- $pages = $pctx.RegularPages }}
{{- else }}
{{- $pages = $pctx.Pages }}
{{- end }}
{{- $limit := site.Config.Services.RSS.Limit }}
{{- if ge $limit 1 }}
{{- $pages = $pages | first $limit }}
{{- end }}
{{- printf "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\"?>" | safeHTML }}
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{{ if eq .Title site.Title }}{{ site.Title }}{{ else }}{{ with .Title }}{{ . }} on {{ end }}{{ site.Title }}{{ end }}</title>
    <link>{{ .Permalink }}</link>
    <description>Recent content {{ if ne .Title site.Title }}{{ with .Title }}in {{ . }} {{ end }}{{ end }}on {{ site.Title }}</description>
    {{- with site.Params.images }}
    <image>
      <title>{{ site.Title }}</title>
      <url>{{ index . 0 | absURL }}</url>
      <link>{{ index . 0 | absURL }}</link>
    </image>
    {{- end }}
    <generator>Hugo -- {{ hugo.Version }}</generator>
    <language>{{ site.Language.LanguageCode }}</language>{{ with $authorEmail }}
    <managingEditor>{{.}}{{ with $authorName }} ({{ . }}){{ end }}</managingEditor>{{ end }}{{ with $authorEmail }}
    <webMaster>{{ . }}{{ with $authorName }} ({{ . }}){{ end }}</webMaster>{{ end }}{{ with site.Copyright }}
    <copyright>{{ . | markdownify | plainify | strings.TrimPrefix "© " }}</copyright>{{ end }}{{ if not .Date.IsZero }}
    <lastBuildDate>{{ (index $pages.ByLastmod.Reverse 0).Lastmod.Format "Mon, 02 Jan 2006 15:04:05 -0700" | safeHTML }}</lastBuildDate>{{ end }}
    {{- with .OutputFormats.Get "RSS" }}
    {{ printf "<atom:link href=%q rel=\"self\" type=%q />" .Permalink .MediaType | safeHTML }}
    {{- end }}
    {{- range $pages }}
    {{- if and (ne .Layout `search`) (ne .Layout `archives`) }}
    <item>
      <title>{{ .Title }}</title>
      <link>{{ .Permalink }}</link>
      <pubDate>{{ .PublishDate.Format "Mon, 02 Jan 2006 15:04:05 -0700" | safeHTML }}</pubDate>
      {{- with $authorEmail }}<author>{{ . }}{{ with $authorName }} ({{ . }}){{ end }}</author>{{ end }}
      <guid>{{ .Permalink }}</guid>
      <description>{{ with .Description | html }}{{ . }}{{ else }}{{ .Summary | html }}{{ end -}}</description>
      {{- if and site.Params.ShowFullTextinRSS .Content }}
      <content:encoded>{{ (printf "<![CDATA[%s]]>" .Content) | safeHTML }}</content:encoded>
      {{- end }}
    </item>
    {{- end }}
    {{- end }}
  </channel>
</rss>
```

## Verification

After placing the file at `hugo-site/layouts/_default/rss.xml`, re-run Hugo on macOS:

```bash
cd /Users/macos/angelife.github.com/hugo-site && hugo
```

Build should complete without the `site.Author` error.